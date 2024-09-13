"""Module that aims to analyze a whole package based 
on the other unitary function of the package"""

from loguru import logger
from pathlib import Path
from tucan.unformat_main import unformat_main
from tucan.struct_main import struct_main
from tucan.imports_main import imports_of_file
from tucan.travel_in_package import clean_extensions_in_paths
from tucan.tucanexceptions import TucanError

def run_full_analysis(files: dict) -> dict:
    """
    Gather the data associated to the functions and the imports within a file

    Args:
        files (dict): key: short_name , value: absolute paths

    Returns:
        dict: _description_
    """

    full_analysis = {}

    skipped_files = []
    unrecoverable_files = []
    for file, path_ in files.items():
        imps,_ = imports_of_file(path_)
        full_analysis[file] = {"imports": imps}
        analysis = struct_main(path_)
        if analysis == {}:
            skipped_files.append(file)
        if analysis == None:
            unrecoverable_files.append(file)
            analysis = {}

        full_analysis[file].update(analysis)
    logger.success("Analyze completed.")
    if unrecoverable_files:
        logger.warning("Some files could not be parsed correctly")
        for f_ in unrecoverable_files + skipped_files:
            print(" - ", f_)

    return full_analysis


def run_unformat(clean_paths: list) -> dict:
    """
    Gather the unformated version of code files within a dict.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as a list of lines with their line number span
    """
    statements = {}
    for file in clean_paths:
        statements[file] = unformat_main(file).to_nob()

        nbr_of_stmt = 0
        if statements[file]:
            nbr_of_stmt = len(statements[file])
        logger.info(f"Found {nbr_of_stmt} statements for {file}")

    return statements


def run_struct(clean_paths: list, ignore_errors:bool=True) -> dict:
    """
    Gather the data associated to the functions within a file.

    Args:
        clean_paths (list): List of cleaned paths.

    Returns:
        dict: File path as key, item as dict with function names and their data (NLOC, CCN, etc.)
    """
    full_struct = {}
    files = []

    for path_ in clean_paths:
        if not Path(path_).is_dir():
            files.append(path_)

    files = clean_extensions_in_paths(files)
    for file in files:
        try:
            full_struct[file] = struct_main(file)
        except TucanError:
            logger.warning(f"Struct analysis failed on {file}")
            if ignore_errors:
                full_struct[file] = {}
            else:
                userinput = input("Would you like to continue (y/n)?")
                if userinput == "y":
                    full_struct[file] = {}
                else:
                    raise # raise previous error

        total_stmts = 0
        for _, data in full_struct[file].items():
            total_stmts += data["ssize"]
        logger.info(f"Found {total_stmts} statements for {file}")

    return full_struct