import re, json
from typing import Tuple, List
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    new_buffer_item,
    new_stack_item,
    struct_from_stack,
    struct_augment,
    list2pathref,
)
from tucan.string_utils import find_words_before_left_parenthesis_noregexp
from tucan.kw_lang import KEYWORDS_C
from tucan.string_utils import tokenize
from tucan.complexities import (
    halstead_numbers,
    halstead_properties,
    compute_cyclomatic_complexity,
    compute_possible_paths,
)

from  tucan.tucanexceptions import TucanCtrlPtsError


def extract_struct_c(stmts: Statements, verbose: bool) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_c.unformat_c
    """

    clean_code = stmts.to_code()
    all_structs = _extract_on_cleaned_c(stmts, verbose=verbose)
    all_structs = struct_augment(
        all_structs,
        clean_code,
        find_callables_c,
        compute_complexities_c,
        compute_cst_ccpp,
    )
    return all_structs


def resolve_scope_resolution(path, name) -> str:
    """find parent if any specified in the name"""
    if "." not in name:
        return None
    parent_path = path + name.split(".")
    in_parent = ".".join(parent_path[:-1])
    # logger.success(f"{name}|->|{in_parent}")
    return in_parent


def _extract_on_cleaned_c(stmts: Statements, verbose: bool = False) -> dict:
    """Extract structure from cleaned statements."""
    buffer = []
    stack = []
    path = []

    stat_idx = 0

    level = 0
    stack_level = [None]
    contains_dict = {}

    for line, (line_idx1, line_idx2) in zip(stmts.stmt, stmts.lines):
        stat_idx += 1
        part = ""

        if "###===" in line:
            type_, name, comment = _parse_type_name_c(line, line_idx1)
            name = name.replace("::", ".")
            # in_parent = resolve_scope_resolution(path,name)
            path.append(name)
            # if in_parent is not None:
            #     if in_parent not in contains_dict:
            #         contains_dict[in_parent] = [list2pathref(path)]
            #     else:
            #         contains_dict[in_parent].append(list2pathref(path))

            stack_level.append(level)
            buffer.append(
                new_buffer_item(
                    type_=type_,
                    path=path,
                    name=name,
                    first_line=line,
                    line_idx=line_idx1,
                    statement_idx=stat_idx,
                    comment=comment,
                    verbose=verbose,
                )
            )
            part = ""

        for char in line:
            part += char
            if char == "{":
                level += 1
            if char == "}":
                level -= 1
                if level == stack_level[-1]:
                    last_buff = buffer[-1]
                    stack.append(
                        new_stack_item(
                            last_buff, line_idx2, stat_idx, line, verbose=verbose
                        )
                    )
                    path.pop(-1)
                    buffer.pop(-1)
                    stack_level.pop(-1)

        # add contains links

    # logger.success(f"Contains {json.dumps(contains_dict, indent=4)}")
    # for stack_item in stack:
    # #    logger.success(f"Trying {stack_item.name}")
    #     if list2pathref(stack_item.path) in contains_dict:
    # #        logger.success(f"Adding contains to {stack_item.name}")
    #         stack_item.contains = contains_dict[list2pathref(stack_item.path) ]

    return struct_from_stack(
        stack,
        main_types=[
            #        "program ",
            #        "module ",
            #        "interface ",
            "int",
            "double",
            "char",
            "float",  # function
            "void",  # subroutine
            "struct",
            "enum",
            "class",
            "template",
            "namespace",  # "userdef_type",
            "pointer",
        ],
    )


def _parse_type_name_c(line: str, line_idx: int) -> Tuple[str, str, str]:
    """expect a lowercase stripped line
    takes the second word as the name

    :: scope resolution is replaced by . to avoid unwanted tokenization of names
    """

    if line.strip() == "":
        return None, None
    tokens = tokenize(line)

    if tokens[0] in ["for", "if", "else", "switch"]:
        return tokens[0], tokens[0] + str(line_idx + 1), None

    if tokens[0] in ["template"]:
        name_, type_, comment = read_template_name_and_type(tokens)
        return "template", name_, type_ + ";" + comment

    try:
        what, who = tokens[0], tokens[1]
    except IndexError:
        msgerr = f"Could not get name from line ({line_idx}){line}"
        raise RuntimeError(msgerr)
    return what, who, None


##### Main structs


def find_callables_c(tokenized_code: List[list]) -> list:
    """Find callables in c"""
    candidates = []
    for tokens in tokenized_code:
        candidates.extend(find_words_before_left_parenthesis_noregexp(tokens))
    matches = [
        cand.strip().replace("::", ".")
        for cand in set(candidates)
        if cand not in KEYWORDS_C
    ]
    # logger.critical(matches)
    return sorted(matches)  # Must be sorted for testing


def build_c_ctrl_points(code: List[list])-> list:
    """build the nested list of control points"""
    listpath=[]
    root_path=[]
    increment_control_pts = ["if",]
    constant_control_pts = ["case", "default"]

    # get exhaustive list of levels
    def _update_current_lvl(current_lvl,tokens):
        new_lvl = current_lvl
        for token in tokens:
            if token == "{":
                new_lvl +=1
            if token == "}":
                new_lvl -=1
        return new_lvl

    # build level information
    last_lvl=0
    levels = [last_lvl]    
    current_lvl = _update_current_lvl(0,code[0])
    for tokens_line in code[1:]:
        levels.append(current_lvl)
        current_lvl =  _update_current_lvl(current_lvl,tokens_line)
        
    # built control list (similiar to python)
    last_lvl=levels[0]
    last_token_line=code[0]
    for current_lvl,tokens_line in zip(levels[1:],code[1:]):
        #print("???",current_lvl,tokens_line)
    
        try: 
            anchor = last_token_line[0]
        except IndexError:
            anchor = None

        if current_lvl > last_lvl:
            root_path.append(anchor)
            listpath.append(root_path.copy())
            #print("+++",root_path)
        
        if tokens_line[0] in constant_control_pts:
            cst_ref= root_path.copy()+[ tokens_line[0]]
            listpath.append(cst_ref)
            #print("===",cst_ref)
        
        if current_lvl<last_lvl:
            while current_lvl<last_lvl:
                try:
                    root_path.pop(-1)
                except IndexError:
                    msg_err="Error while building controlpoints."
                    logger.warning(msg_err)
                    raise TucanCtrlPtsError(msg_err)
                last_lvl-=1
        
        last_lvl=current_lvl
        last_token_line=tokens_line

    # # remove non-control-points levels  
    # for path in  listpath:
    #     print("raw :",path)


    clean_list_path=[]   
    for i,path in enumerate(listpath):
        purged =  [item for item in path if item in increment_control_pts+constant_control_pts]
        if purged == [] :
            continue
        if not clean_list_path:
            clean_list_path.append(purged.copy())
            continue

        if purged[-1] in constant_control_pts:
            clean_list_path.append(purged.copy())
        elif purged != clean_list_path[-1]:
            clean_list_path.append(purged.copy())
           
    # for path in  clean_list_path:
    #     print("clean:",path)

    ctrl_points = [[]]
    for path in clean_list_path:
        if path == []:
            continue
        inserter=ctrl_points
        for _ in path:
            inserter=inserter[-1]
        inserter.extend([path[-1],[]])
    ctrl_points=ctrl_points[0]
 
    return ctrl_points


def compute_complexities_c(indents_code: List[int], tokenized_code: List[list]) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    avg_indent = sum(indents_code)/len(indents_code)/2
    ctrls_pts = build_c_ctrl_points(tokenized_code)
    mccabe = compute_cyclomatic_complexity(ctrls_pts)
    possible_paths = compute_possible_paths(ctrls_pts)
    volume, difficulty, effort =  halstead_properties(*halstead_numbers(tokenized_code, KEYWORDS_C))
    time_to_code = int(effort/18)

    return round(avg_indent,2),mccabe,possible_paths,volume, difficulty,time_to_code


# def compute_ccn_approx_c(code: list) -> int:
#     """Count decision points (if, else if, do, select, etc.)"""
#     decision_points = re.findall(
#         r"(?i)(if |else |for |case |default )", "\n".join(code)
#     )
#     complexity = len(decision_points) + 1
#     return complexity


def read_template_name_and_type(tokens) -> Tuple[str, str, str]:
    """Extract template name and typology form the declaration"""
    # read template defs

    comment = ""
    if "static" in tokens:
        comment += "static"

    tokens = [token for token in tokens if token not in ["static", "inline"]]

    assert tokens[0] == "template"
    idx = 1

    if tokens[idx] == "<":
        content0, idx = read_chevrons(tokens, start=idx)
        comment += "<" + ",".join(content0) + ">"
    else:
        content0 = []
    idx += 1

    # read template first element (type for a function, name for a constructor)
    tok_1 = tokens[idx]
    idx += 1
    if tokens[idx] == "(":  # assumes it is a constructor
        return tok_1, "constructor", comment
    else:
        type_ = tok_1

    if tokens[idx] == "<":
        content, idx = read_chevrons(tokens, start=idx)
        if content:
            type_ = "<" + " ".join(content) + ">" + type_

    # read template name
    name = tokens[idx]
    if name == "&":
        idx += 1
        name = "&" + tokens[idx]
    # if content0:
    #     name += "."+"|".join(content0)

    idx += 1
    if tokens[idx] == "<":
        content, idx = read_chevrons(tokens, start=idx)
        if content:
            name = name + ".<" + " ".join(content) + ">"
    else:
        content = ""

    return name, type_, comment


def read_chevrons(list_, start=0) -> Tuple[list, int]:
    """Read chevrons declarations in cpp code, especially in the context of templates"""
    assert list_[start] == "<"
    end_idx = list_.index(">", start)
    idx = start
    content = []
    while idx < end_idx:
        if list_[idx] == "=":
            idx += 2
            continue
        if list_[idx] not in ["<", "typename", ",", "=", "..."]:
            content.append(list_[idx])
        idx += 1

    joined_content = []
    join = False
    for item in content:
        if item in ["::"]:
            join = True
        else:
            if join:
                joined_content[-1] += "::" + item
                join = False
            else:
                joined_content.append(item)

    return joined_content, idx


def compute_cst_ccpp(type_: str) -> int:
    """State the structural complexity of a code

    in Short, the average nb. of time we re-read the element.
    It does NOT means it's bad practice
    It just means more read time for the reader to understand the code"""

    cst_ = {
        "int": 1,
        "double": 1,
        "char": 1,
        "float": 1,
        "void": 2,
        "namespace": 2,
        "pointer": 2,
        "enum": 2,
        "struct": 3,
        "class": 4,
        "template": 8,
    }
    if type_ not in cst_:
        logger.warning(f"Type {type_} not present in conversion list ")
        return 1

    return cst_.get(type_, 1)
