"""
Tucan module to get the imports of a python file
"""
from typing import List
from tucan.string_utils import tokenize
from loguru import logger

def by_cpp_include(tokens):
    """Resolve a CPP include import, also used in Fortran"""
    # namespaces
    if tokens[2] == "<":
        ref = tokens[3]
    else:
        ref = tokens[2].strip("'").strip('"')

    ref = ref.replace("../","")
    return {f"_{ref}": ref+"@*"}


def get_imports_ccpp(lines: List[str]) -> dict:
    """Read the imports information from C/C++ lines"""
    out = {}
    for line in lines:
        if line.lstrip().startswith("#"):
            line = line.replace("<","'").replace(">","'")
            tokens = tokenize(line)
            if tokens[1] in ["include", "INCLUDE"]:
                out.update(by_cpp_include(tokens))
    return out
