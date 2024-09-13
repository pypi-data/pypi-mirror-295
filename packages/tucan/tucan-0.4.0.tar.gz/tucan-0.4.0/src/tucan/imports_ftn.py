"""
Tucan module to get the imports of a fortran file
"""
from loguru import logger
from typing import List
from tucan.string_utils import tokenize
from tucan.unformat_common import Statements
from tucan.imports_c import by_cpp_include


def _by_use(tokens):
    """Resolve a Fortran use import"""
    # namespaces

    re_tokens = [
        token for token in tokens if token not in [",", ":", "::"]
    ]

    out = {}
    if "intrinsic" in re_tokens or "INTRINSIC" in re_tokens:
        for i in range(2, len(re_tokens), 1):
            #out[re_tokens[i]] = f"__intrinsic__.{re_tokens[i]}"
            out[re_tokens[i]] = f"__ftn__@__intrinsic__.{re_tokens[i]}"
        return out

    ref = re_tokens[1]
    if "only" in re_tokens or "ONLY" in re_tokens:
        for i in range(3, len(re_tokens), 1):
            #out[re_tokens[i]] = f"{ref}.{re_tokens[i]}"
            out[re_tokens[i]] = f"__ftn__@{ref}.{re_tokens[i]}"
            
    else:
        #out[f"_{ref}"] = ref
        out[f"_{ref}"] = f"__ftn__@{ref}"

    return out


def _by_include(tokens):
    """Resolve a Fortran include  import"""
    # namespaces
    ref = tokens[1].strip("'").strip('"')
    #return {f"_{ref}": ref}
    return {f"_{ref}": ref+"@*"}


def get_imports_ftn(lines: List[str],verbose=False) -> dict:
    """Read the imports information from python lines"""
    out = {}
    for i,line in enumerate(lines):
        if line.lstrip().replace(" ","").startswith(("use", "#include", "include","USE", "#INCLUDE", "INCLUDE")):
            tokens = tokenize(line)
            try:
                if tokens[0] in ["use", "USE"]:
                    out.update(_by_use(tokens))
                elif tokens[0] in ["include", "INCLUDE"]:
                    out.update(_by_include(tokens))
                elif tokens[1] in ["include", "INCLUDE"]:
                    out.update(by_cpp_include(tokens))
            except IndexError:
                pass

    return out
