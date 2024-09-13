"""
Module that gather the most common functions of struct.
"""

from dataclasses import dataclass
from typing import Tuple, List, Callable
from copy import deepcopy
from loguru import logger
from typing import List
from tucan.complexities import maintainability_index
from tucan.string_utils import tokenize, get_indent

def path_clean(path: list, paths_to_clean: Tuple[list]) -> list:
    """Remove the unwanted steps of the paths"""
    indexes_to_clean = []
    for ptc in paths_to_clean:
        if list2pathref(path).startswith(list2pathref(ptc)):
            indexes_to_clean.append(len(ptc) - 1)
    new_path = []
    for i, step in enumerate(path):
        if i not in indexes_to_clean:
            new_path.append(step)
    return new_path


def list2pathref(path: list) -> str:
    """The way we will refer to path here in strings"""
    return ".".join(path)


def pathref_ascendants(pathstr: str) -> List[str]:
    """Return all ascendends of a path"""
    out = []
    path = pathstr.split(".")
    while len(path) > 1:
        path.pop(-1)
        out.append(list2pathref(path))
    return out



def show_time(timesec:int)->str:
    out = str(timesec) + " seconds"
    if timesec >= 60:
        out = f"{int(timesec/60):4g} min"
    if timesec >= 3600:
        out = f"{int(timesec/3600):4g} hrs"
    if timesec >= 3600*24:
        out = f"{(int(timesec/(3600*24))):4g}days"
    return out



def struct_summary_str(main_structs: dict) -> str:
    out = []

    if main_structs is None:
        return "No structure data is available. Tucan light parser could not interpret this file."
    for part, data in main_structs.items():
        out.append(f'\n{data["type"]} {part} :')
        out.append(
            f'    At path {data["path"]}, name {data["name"]}, lines {data["lines"][0]} -> {data["lines"][-1]}'
        )
        out.append(f'    {data["ssize"]} statements over {data["NLOC"]} lines')
        out.append("    >>> Complexity <<<")
        
        out.append(
            f'    Mcabe ctrlPts  CCN: {data["CCN"]:8d} (inside),   {data["CCN_int"]:8g} (CCN_int intensive)'
        )
        out.append(
            f'    PossiblePaths  CPP: {data["CPP"]:8g} (inside),   {data["CPP_int"]:8g} (CPP_int intensive)'
        )
        out.append(
            f'    Halstead Diff. HDF: {data["HDF"]:8g} (inside),   {data["HDF_int"]:8g} (HDF_int intensive)'
        )
        out.append(
            f'    Avg. Indents.  IDT: {data["IDT"]:8g} (inside),   {data["IDT_int"]:8g} (IDT_int intensive)'
        )
        out.append(
            f'    Struct Cplx.   CST: {data["CST"]:8g} (inside),   {data["CST_ext"]:8g} (CST_ext extensive)'
        )
        out.append(
            f'    Maintn. Index  MI : {data["MI"]:8g} (inside),   {data["MI_int"]:8g} ( MI_int intensive)'
        )
        out.append(
            f'    Halstead Time. HTM: {show_time(data["HTM"])} (inside),   {show_time(data["HTM_ext"])} (HTM_ext extensive)'
        )
        
        
        if data["callables"]:
            list_str = "\n       - " + "\n       - ".join(data["callables"])

            out.append(f'    Refers to {len(data["callables"])} callables:{list_str}')

        if data["contains"]:
            list_str = "\n    - " + "\n    - ".join(data["contains"])
            out.append(f'    Contains {len(data["contains"])} elements:{list_str}')

        if data["parents"]:
            list_str = "\n       - " + "\n       - ".join(data["parents"])
            out.append(f'    Refers to {len(data["parents"])} parents:{list_str}')

        if data["annotations"]:
            keyvals = [
                key + ":" + values for key, values in data["annotations"].items()
            ]
            list_str = "\n       - " + "\n       - ".join(keyvals)

            out.append(f"    Refers to {len(keyvals)} callables:{list_str}")

    return "\n".join(out)


########################################################
# BUFFER of detection
@dataclass
class BufferItem:
    """Forces buffers to keep the same logic across languages"""

    type_: str = None
    name: str = None
    path: list = None
    first_line: str = None
    line_idx: int = None
    statement_idx: int = None
    parents: List[str] = None
    callables: List[str] = None
    contains: List[str] = None
    comment: str = None


def new_buffer_item(
    type_: str = None,
    name: str = None,
    path: List[str] = None,
    first_line: str = None,
    line_idx: int = None,
    statement_idx: int = None,
    verbose: bool = False,
    parents: List[str] = None,
    callables: List[str] = None,
    contains: List[str] = None,
    comment: str = None,
) -> BufferItem:
    if verbose:
        fname = ".".join(path)
        logger.critical(f"START l.{line_idx} for " + fname)
    if parents is None:
        parents = []
    if callables is None:
        callables = []
    if contains is None:
        contains = []
    if comment is None:
        comment = ""
    out = BufferItem(
        type_=type_,
        name=name,
        path=path,
        first_line=first_line,
        line_idx=line_idx,
        statement_idx=statement_idx,
        parents=parents,
        callables=callables,
        contains=contains,
        comment=comment,
    )
    return out


########################################################
# STACK of detection
@dataclass
class StackItem:
    """Forces buffers to keep the same logic across languages"""

    type_: str
    name: str
    path: list
    start_line_idx: int
    start_statement_idx: int
    start_line: str
    end_line_idx: int
    end_statement_idx: int
    end_line: str
    parents: List[str] = None
    callables: List[str] = None
    contains: List[str] = None
    comment: str = None


def new_stack_item(
    buf: BufferItem,
    end_line_idx: int,
    end_statement_idx: int,
    end_line: str,
    verbose: bool = False,
) -> StackItem:
    if verbose:
        fname = ".".join(buf.path)
        logger.critical(f" END   l.{end_line_idx} for " + fname + '|'+end_line.strip())
    out = StackItem(
        type_=buf.type_,
        name=buf.name,
        path=buf.path.copy(),
        start_line_idx=buf.line_idx,
        start_statement_idx=buf.statement_idx,
        start_line=buf.first_line,
        parents=buf.parents,
        callables=buf.callables,
        contains=buf.contains,
        comment=buf.comment,
        end_line_idx=end_line_idx,
        end_statement_idx=end_statement_idx,
        end_line=end_line,
    )
    return out


def struct_from_stack(stack: list, main_types: list, skip_types: list = None) -> dict:
    """Build a dictionary of all structures"""
    # Build nested structure
    struct = {}
    if skip_types is None:
        skip_types = []

    path_to_skip = []
    for stack_item in stack:
        if stack_item.type_ in skip_types:
            path_to_skip.append(stack_item.path)

    for stack_item in stack:
        cleaned_path = path_clean(stack_item.path, path_to_skip)
        if stack_item.type_ in main_types:
            # logger.warning(f"Adding {list2pathref(cleaned_path)}")
            id_ = list2pathref(cleaned_path)
            if id_ not in struct:
                struct[id_] = {
                    "path": cleaned_path,
                    "name": stack_item.name,
                    "type": stack_item.type_,
                    "linestart": stack_item.start_line,
                    "lines": [stack_item.start_line_idx, stack_item.end_line_idx],
                    "statements": [
                        stack_item.start_statement_idx,
                        stack_item.end_statement_idx,
                    ],  # Warning: here statements starts at 1!!!
                    "contains": stack_item.contains,
                    "parents": stack_item.parents,
                    "callables": stack_item.callables,
                    "comment": stack_item.comment,
                    "annotations": {},
                }
            else: # create a proxy because this structure is redefined
                id_new = id_ + f"#{stack_item.start_line_idx},{stack_item.end_line_idx}"
                struct[id_new] = {
                    "path": cleaned_path,
                    "name": stack_item.name,
                    "type": stack_item.type_,
                    "linestart": stack_item.start_line,
                    "lines": [stack_item.start_line_idx, stack_item.end_line_idx],
                    "statements": [
                        stack_item.start_statement_idx,
                        stack_item.end_statement_idx,
                    ],  # Warning: here statements starts at 1!!!
                    "contains": stack_item.contains,
                    "parents": stack_item.parents,
                    "callables": stack_item.callables,
                    "comment": stack_item.comment,
                    "annotations": {},
                }
                struct[id_]["contains"].append(id_new)
            
           

    return struct


def get_struct_sizes(struct: dict) -> dict:
    """Compute the size of strict items (statefull)"""
    struct_aspects = {}
    for part, data in struct.items():
        struct_aspects[part] = {}
        struct_aspects[part]["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
        struct_aspects[part]["ssize"] = data["statements"][-1] - data["statements"][0]
        
    return struct_aspects


def replace_self(list_: list, parent: str) -> list:
    """Replace the self keyword in a parentality path"""
    return [item.replace("self.", parent + ".") for item in list_]


def _strip_safe_lines(beg: int, end: int, safes: List[list]) -> List:
    """Return an iterable stripped from safe zones
    beg=100
    end = 110
    safes = [[103,104],[106,109]]

    100
    101
    102
    105

    """
    iter_ = []
    for i in range(beg, end + 1):
        blocked = False
        for safe in safes:
            if i >= safe[0] and i <= safe[1]:
                # print(f"{i} blocked")
                blocked = True
        if not blocked:
            iter_.append(i)
    return iter_


def struct_actual_lines(struct_in: dict, name: str) -> list:
    """returns an iterable with only the statement relative to this part
    excluding contained parts.

    WARNING:The -1 on statements is systematic because statements numbering is starting at 1
    """
    data = struct_in[name]
    safes = []
    for sub_name in data["contains"]:
        try:
            safes.append(
                [
                    struct_in[sub_name]["statements"][0] - 1,
                    struct_in[sub_name]["statements"][1] - 1,
                ]
            )
        except KeyError:
            msgerr = f"Item {sub_name} is not referenced in this context"
            raise RuntimeError(msgerr)

    return _strip_safe_lines(
        data["statements"][0] - 1, data["statements"][1] - 1, safes
    )


def struct_augment(
    struct_in: dict,
    clean_code: List[str],
    find_callables: Callable,
    compute_complexities: Callable,
    compute_cst: Callable,
) -> dict:
    """Complete the description of each struct item"""
    struct = deepcopy(struct_in)
    # first lines computation
    for _, data in struct.items():
        data["NLOC"] = data["lines"][-1] - data["lines"][0] + 1
        data["ssize"] = data["statements"][-1] - data["statements"][0] + 1

    # add internal links
    for part, data in struct.items():
        path = data["path"]
        # logger.warning(path)

        if len(path) > 1:
            parent = path[:-1] + path[-1].split(".")[:-1]
            try:
                struct[list2pathref(parent)]["contains"].append(list2pathref(path))
                # pass
            except KeyError:
                pass
                # will happen for scripts, with "dummy" not always referenced.
            # struct[part]["parents"].append(list2pathref(parent))
        # else:
        #     struct[part]["parent"]=None

    # add language specific analyses
    for part, data in struct.items():
        actual_lines = struct_actual_lines(struct, part)
        sub_code = [clean_code[i] for i in actual_lines]
       # logger.critical(part)
        # for i,line in enumerate(clean_code):
        #     if i  in actual_lines:
        #         logger.success(line)
        #     else:
        #         logger.warning(line)

        sub_tokenized_code = [tokenize(line) for line in sub_code[1:]]
        sub_indents_code=  [ len(get_indent(line)) for line in sub_code[1:]]

       
        data["callables"].extend(find_callables(sub_tokenized_code))
        if data["parents"]:
            data["callables"] = replace_self(data["callables"], data["parents"][0])
        if data["type"] in ["class"]:
            data["contains"] = replace_self(data["contains"], part)
            data["callables"] = replace_self(data["callables"], part)

        if len(sub_tokenized_code)==0:
            avg_indent=0
            mccabe=1
            possible_paths=1
            volume=0
            difficulty=0
            time_to_code=0
        else:
            avg_indent,mccabe,possible_paths,volume, difficulty,time_to_code=compute_complexities(sub_indents_code,sub_tokenized_code)
        data["CCN"] = mccabe
        data["IDT"] = avg_indent
        data["CPP"] = possible_paths
        data["HDF"] = difficulty
        data["HTM"] = time_to_code
        data["CST"] = compute_cst(data["type"])
        data["MI"] = maintainability_index(volume,mccabe, data["ssize"])
        
    



    fields_intensive = ["CCN","CPP","HDF","MI","IDT"]
    fields_extensive = ["HTM","CST"]
    def recursive_aggregate(struct, label):
        if "aggregated" not in struct[label]:
            sums_ext = {field:0 for field in fields_extensive}
            sums_int = {field:0 for field in fields_intensive}

            for child in struct[label]["contains"]:
                recursive_aggregate(struct, child)
                sums_ext = {field: sums_ext[field]+struct[child][field]  for field in fields_extensive}
                sums_int = {field: sums_int[field]+struct[child][field]*struct[child]["ssize"]  for field in fields_intensive}

            for field in fields_extensive:
                struct[label][field+"_ext"]= sums_ext[field]+ struct[label][field]
            for field in fields_intensive:
                struct[label][field+"_int"]= round(sums_int[field] /struct[label]["ssize"] + struct[label][field],2)

            struct[label]["aggregated"]=True

                
    for part in struct.keys():
        if "aggregated" not in struct[part]:
            recursive_aggregate(struct, part)


    return struct
