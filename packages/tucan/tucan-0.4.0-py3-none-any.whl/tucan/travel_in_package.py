
from pathlib import Path
from loguru import logger


def rec_travel_through_package(
    path: str,
    optional_paths: list = None,
) -> list:
    """
    List all paths from a folder and its sub-folders recursively.

    RECURSIVE
    """
    if not optional_paths:
        optional_paths = []

    current_paths_list = [path, *optional_paths]

    # Move to absolute Path objects
    current_paths_list = [Path(p_) for p_ in current_paths_list]

    accepted_suffixes = ["f","f90","f77", "c","cc", "cpp","h","hpp","py"]

    paths_ = []
    for current_path in current_paths_list:
        for element in current_path.iterdir():
            if element.is_dir():
                path_str = element.as_posix()
                paths_.extend(rec_travel_through_package(path_str))
            else:
                if element.as_posix().split(".")[-1].lower() not in accepted_suffixes:
                    continue
                if element.as_posix() not in paths_:
                    if not element.as_posix().split("/")[-1].startswith("."):
                        paths_.append(element.as_posix())
    return paths_


def clean_extensions_in_paths(paths_list: list) -> list:
    """
    Remove unwanted path extensions and duplicates.

    Args:
        paths_list (list): List of all paths gatheres through recursive analysis

    Returns:
        list: List of cleaned paths.
    """
    clean_paths = []
    for path in paths_list:
        if path.endswith(
            (
                ".py",
                ".f",
                ".F",
                ".f77",
                ".f90",
                ".F77",
                ".F90",
                ".c",
                ".cpp",
                ".h",
                ".hpp",
            )
        ):
            clean_paths.append(path)

    return [
        *set(clean_paths),
    ]


def get_package_files(clean_paths: list, relpath: str) -> dict:
    """
    Return all the files useful for a package analysis, with their absolut paths
    """

    files = []
    for path_ in clean_paths:
        if not Path(path_).is_dir():
            #            logger.info(f"Append :{path_}")
            files.append(path_)

    files = clean_extensions_in_paths(files)

    if not files:
        logger.warning(f"No files found in the paths provided")

    files = [Path(relpath) / Path(p_) for p_ in files]

    out = {}
    for file in files:
        path_ = file.relative_to(Path(relpath)).as_posix()
        out[path_] = file.as_posix()
    return out
