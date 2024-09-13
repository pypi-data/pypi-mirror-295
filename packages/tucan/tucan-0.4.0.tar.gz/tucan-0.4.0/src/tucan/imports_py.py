"""
Tucan module to get the imports of a python file
"""

from typing import List

# from tucan.unformat_common import Statements
from tucan.string_utils import tokenize

# def imports_py(statements: Statements) -> dict:
#     """
#     Main function to search the imports in a python file.

#     Args:
#         statements (Statements): List of unformatted code statements along with line number ranges.

#     Returns:
#         dict: Dict with the module or function name associated with its various imports.
#     """
#     imports_dict = python_imports(statements)

#     return imports_dict


# def python_imports(stmts: Statements) -> dict:
#     """
#     Parse the python code to check for the imports and update the imports database.

#     Args:
#         stmts (Statements): List of unformatted code statements along with line number ranges.

#     Returns:
#         imports_dict (dict): Dict with the module or function name associated with its various imports.
#     """
#     imports_dict = {}
#     for line in stmts.stmt:
#         if "import " not in line:
#             pass

#         # Parsing "as" imports (ex: numpy as np) for later identification
#         if line.strip().startswith("import "):
#             module_from = line.split("import ")[-1].strip()
#             if " as " in line:
#                 alias = line.split(" as ")[-1].strip()
#                 module_from = module_from.split(" as ")[0].strip()
#                 imports_dict[module_from] = {"alias": alias, "explicit": []}
#             else:
#                 module_from = module_from.split(",")
#                 for mod_from in module_from:
#                     imports_dict[mod_from.strip()] = {"explicit": []}

#         # Parsing "from XXX import XXX", i.e. specific imports
#         if line.strip().startswith("from ") and "import" in line.strip():
#             module_from = line.split("import ")[0].split("from ")[-1].strip()
#             func_imported = line.split("import ")[1:]
#             # Handle the case from XXXX import XXXX as XXXX
#             if "as " in func_imported[0]:
#                 mod_and_alias = func_imported[0].split("as ")
#                 func_imported = {
#                     "alias": mod_and_alias[1].strip(),
#                     "explicit": [mod_and_alias[0].strip()],
#                 }  # Name of function is saved not the alias yet

#             # Handle imports on multiple lines
#             elif func_imported[0].startswith("("):
#                 func_imported = func_imported[0].split("(")[-1]
#                 func_imported = func_imported.split(")")[0]
#                 func_imported = {
#                     "explicit": [func_.strip() for func_ in func_imported.split(",")]
#                 }

#             else:
#                 func_imported = func_imported[0].split(",")
#                 func_imported = {"explicit": [func_.strip() for func_ in func_imported]}

#             imports_dict[module_from] = func_imported

#     return imports_dict


def _by_import(tokens):
    """Resolve a Python direct import line"""
    # namespaces
    if "as" in tokens:

        if len(tokens) != 4:
            line = " ".join(tokens)
            raise RuntimeError(f"Unexpected situation: {line}")
        init_ref = tokens[1]
        ref = tokens[1].split(".")[0]
        #return {tokens[3]: f"{ref}.{tokens[1]}"}
        return {tokens[3]: f"__py__@{tokens[1]}"}

    # multiple imports
    if "," in tokens:
        out = {}
        for token in tokens:
            if token not in ["import", ",", "(", ")"]:
                #out[token] = token
                out[token] = f"__py__@{token}"
        return out
    # default
    ref = tokens[1].split(".")[0]
        
    return {tokens[1]: f"__py__@{tokens[1]}"}


def _by_from(tokens):
    """Resolve a Python from import line"""
    # namespaces

    retokens = [tok for tok in tokens if tok not in [",", "(", ")"]]

    ref = retokens[1].lstrip(".")

    out = {}
    if "as" in retokens:
        idx = retokens.index("as")
        for i in range(0, idx - 3):
            name = retokens[3 + i]
            alias = retokens[idx + 1 + i]
            out[alias] = f"__py__@{ref}.{name}"
    else:
        if retokens[3] == "*":
            return {f"_{ref}": f"__py__@{ref}.*"}
          
        for i in range(0, len(retokens) - 3):
            name = retokens[3 + i]
            out[name] = f"__py__@{ref}.{name}"

    return out


def get_imports_py(lines: List[str]) -> dict:
    """Read the imports information from python lines"""
    out = {}
    for line in lines:
        if line.lstrip().startswith(("from", "import")):
            tokens = tokenize(line)
            if tokens[0] == "import":
                out.update(_by_import(tokens))
            if tokens[0] == "from":
                out.update(_by_from(tokens))

    return out
