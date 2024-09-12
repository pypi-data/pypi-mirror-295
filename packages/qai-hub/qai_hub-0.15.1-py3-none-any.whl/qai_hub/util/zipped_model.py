import os
from contextlib import contextmanager
from pathlib import Path
from shutil import make_archive
from tempfile import TemporaryDirectory
from zipfile import ZipFile

SUPPORTED_ZIPPED_MODEL_ASSETS = {
    ".mlmodelc",
    ".mlpackage",
    ".trtmodel",
    ".aimet",
    ".onnx",
}


def zip_model(output_dir_path: str, model_path: str) -> str:
    """
    Zips directory model_path as a base directory.
    Example:
        output_dir_path: "/path/to/out/"
        model_path : "/path/to/model1/model_123.mlmodelc"
        creates following zip file at location "/path/to/out/model_123.zip":
            model_123.zip
                -> model_123.mlmodelc

    Parameters
    ----------
        output_dir_path (str): output directory path to create new archive
        model_path (str): source model path to archive

    Returns
    -------
        zipped_model_path (str): returns zipped file path
    """

    model_path = os.path.realpath(model_path)
    package_name = os.path.basename(model_path)

    # archive name with model extensions
    archive_base_name = os.path.join(output_dir_path, package_name)
    return make_archive(
        base_name=archive_base_name,
        format="zip",
        root_dir=os.path.dirname(model_path),
        base_dir=package_name,
    )


def unzip_model(
    zipped_model_path: str,
    path_to_extract: str,
) -> str:
    """
    Extracts zipped model at provided path
    Example:
        zipped_model_path: "/path/to/input/any_name.mlpackage.zip"
        content of zip file:
            any_name.mlpackage.zip
                -> model.mlpackage
        path_to_extract : "/path/to/out/"
        extracts model.mlpackage.zip at "/path/to/out/model.mlpackage"

    Parameters
    ----------
        zipped_model_path (str): input zipped model to extract
        path_to_extract (str): directory to extract model to

    Returns
    -------
        unzipped_model_path (str): returns unzipped model path

    Raises
    ------
    ValueError
        If only one supported model asset is not present at base path zipped file
    """

    with ZipFile(zipped_model_path) as zippedFile:
        model_zip_content = list(
            set(
                [
                    os.path.normpath(name).split(os.sep)[0]
                    for name in zippedFile.namelist()
                ]
            )
        )

        if len(model_zip_content) != 1:
            raise ValueError(
                "Invalid archived model. "
                f"Expecting only one model asset at base path {SUPPORTED_ZIPPED_MODEL_ASSETS}."
            )

        model_asset_path = list(model_zip_content)[0]
        zippedFile.extractall(path_to_extract)
        return os.path.join(path_to_extract, model_asset_path)


@contextmanager
def zip_model_if_necessary(model_path):
    """
    Zips up a model if necessary. This is a context manager that yields a
    (path, is_directory) pair. The path may refer to a temporary directory
    that is cleaned up by the context manager.
    """
    if os.path.isdir(model_path):
        with TemporaryDirectory() as tmp_dir:
            output_model_path = zip_model(tmp_dir, model_path)
            yield (output_model_path, True)
    else:
        yield (model_path, False)


def make_zipped_model_compatible(
    input_zipped_model_path: str,
    output_model_dir_path: str,
):
    """
    Make existing archive compatible with hub
    i.e. only keep one model asset at base path.
    Certain OSes inserts metadata during compression, which we would like to
    remove here e.g. macOS inserts `__MACOS__` directory during compression.

    Example:
        input_archived_model.zip
            -> __MACOS__/
            -> model.mlpackage/
            -> some_metadata_file
        output_archived_model.zip
            -> model.mlpackage/

    Parameters
    ----------
        input_zipped_model_path (str): input zipped model path
        output_model_dir_path (str): output model directory path to serialize new zipped model
            if needed.

    Returns
    -------
        Return path to compatible zip file which is:
            * input_zipped_model_path if input zip is already compatible
            * new zip file serialized at output_model_dir_path directory

    Raises
    ------
    ValueError
        If input archive has more than one model asset at base path
    """

    with ZipFile(input_zipped_model_path) as zippedFile:
        model_zip_content = list(
            set(
                [
                    os.path.normpath(name).split(os.sep)[0]
                    for name in zippedFile.namelist()
                ]
            )
        )

        if (
            len(model_zip_content) == 1
            and Path(model_zip_content[0]).suffix in SUPPORTED_ZIPPED_MODEL_ASSETS
        ):
            # input archived model is compatible
            return input_zipped_model_path

        model_paths = [
            name
            for name in model_zip_content
            if Path(name).suffix in SUPPORTED_ZIPPED_MODEL_ASSETS
        ]
        if len(model_paths) != 1:
            raise ValueError(
                "Incorrect archived model. "
                "Archived model must have only one base level <model>.<model_extension> asset."
            )
        model_path = model_paths[0]

        with TemporaryDirectory() as tempdir:
            zippedFile.extractall(tempdir)
            return zip_model(
                str(Path(output_model_dir_path).with_suffix("")),
                str(os.path.join(tempdir, model_path)),
            )


def check_onnx_directory_contents(path):
    onnx_files = [f for f in os.listdir(path) if f.endswith(".onnx")]
    context_binary_files = [f for f in os.listdir(path) if f.endswith(".bin")]
    if len(onnx_files) != 1:
        raise ValueError(f".onnx path must contain exactly one .onnx file: {path}")
    if len(context_binary_files) != 1:
        raise ValueError(f".onnx path must contain exactly one .onnx file: {path}")
    if (
        os.path.splitext(context_binary_files[0])[0]
        == os.path.splitext(onnx_files[0])[0]
    ):
        raise ValueError(".onnx file and .bin file must have the same name.")
    return True


def validate_model_with_onnx_ext(path):
    # Check inside to determine if its ONNX directory created is correct.
    if not os.path.isdir(path):
        try:
            with TemporaryDirectory() as tempdir:
                unzip_model(path, tempdir)
                subdir = next(os.scandir(tempdir)).name
                subdir_path = os.path.join(tempdir, subdir)
                return True if check_onnx_directory_contents(subdir_path) else False
        except Exception:
            # The model is not .onnx directory
            return True
        else:
            return True if check_onnx_directory_contents(subdir_path) else False
