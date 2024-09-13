import re
from typing import Tuple, List
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    new_buffer_item,
    new_stack_item,
    struct_from_stack,
    struct_augment,
)
from tucan.unformat_common import rm_parenthesis_content
from tucan.string_utils import find_words_before_left_parenthesis_noregexp, tokenize
from tucan.tucanexceptions import TucanParsingError,TucanCtrlPtsError

from tucan.kw_lang import STRUCTURES_FTN, NESTS_FTN, OTHERS_FTN
from tucan.complexities import (
    halstead_numbers,
    halstead_properties,
    compute_cyclomatic_complexity,
    compute_possible_paths,
)


PARTS = sorted(STRUCTURES_FTN, reverse=True)
NESTS = sorted(NESTS_FTN, reverse=True)
INTRINSICS = OTHERS_FTN


def extract_struct_ftn(stmts: Statements, verbose) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_ftn.unformat_ftn
    """
    clean_code = stmts.to_code()

    all_structs = _extract_on_cleaned_ftn(stmts, verbose=verbose)
    all_structs = struct_augment(
        all_structs,
        clean_code,
        find_callables_ftn,
        compute_complexities_ftn,
        compute_cst_ftn,
    )
    return all_structs


def _extract_on_cleaned_ftn(stmts: Statements, verbose=False) -> dict:
    """Extract structure from cleaned statements."""
    buffer_pile = []
    stack = []
    path = []

    ins_ = []
    out_ = []
    stat_idx = 0
    for line, (line_idx1, line_idx2) in zip(stmts.stmt, stmts.lines):
        stat_idx += 1

        line = line.lstrip(" ")

        # you must also note nests because bare end statement can jam the system
        # kw are listed in reverse order to try longer kwords first: type_real before
        # for part in sorted(STRUCTURES_FTN + NESTS_FTN, reverse=True):
        for part in sorted(PARTS + NESTS, reverse=True):
            if line.startswith(part + " ") or line == part:
                ins_.append(line)
                name, type_ = _parse_name_ftn(line, line_idx1)
                path.append(name)
                buffer_pile.append(
                    new_buffer_item(
                        type_=type_,
                        path=path,
                        name=name,
                        first_line=line,
                        line_idx=line_idx1,
                        statement_idx=stat_idx,
                        verbose=verbose,
                    )
                )
                break  # must not look at the following part, or both function and function_elemental will trigger

        if "procedure" in line:
            tokens = tokenize(line)
            if "=>" in tokens:
                idx = tokens.index("=>")
                target = tokens[idx + 1]
                proxy = tokens[idx - 1]
            else:
                target = tokens[-1]
                proxy = tokens[-1]

            target_name = ".".join(path[:-1]) + "." + target
            proxy_name = ".".join(path) + "." + proxy
            path.append(proxy)
            last_buff = buffer_pile[-1]

            # logger.warning(f"Adding proxy {proxy_name} (pointer to {target_name}) to {last_buff.name}")

            buf_ = new_buffer_item(
                type_="procedure",
                path=path,
                name=proxy_name,
                first_line=line,
                line_idx=line_idx1,
                statement_idx=stat_idx,
                verbose=verbose,
                callables=[target_name],
            )
            stack.append(
                new_stack_item(buf_, line_idx1, stat_idx, line, verbose=verbose)
            )
            path.pop(-1)

        if line.startswith("__type_from__"):
            parent = tokenize(line)[2]
            # logger.warning(f"Adding parent {parent}")
            if parent not in buffer_pile[-1].parents:
                buffer_pile[-1].parents.append(parent)

        if line.startswith("type") and "extends" in line:
            strt_ = line.index("extends")
            read = False
            parent = ""
            for char in line[strt_:]:
                if char == "(":
                    read = True
                elif char == ")":
                    break
                else:
                    if read:
                        parent += char
            parent = parent.strip()
            # logger.warning(f"Adding parent {parent}")
            if parent not in buffer_pile[-1].parents:
                buffer_pile[-1].parents.append(parent)

        if line.startswith("end ") or line.strip() == "end":
            
            if not buffer_pile:
                msg = f"No code read matching END statement {line_idx1}:{line}"
                logger.critical(msg)
                raise TucanParsingError(msg)
            
            last_buff = buffer_pile[-1]  # Here
            
            items=line.split()
            if len(items)>=2:
                expected_type = last_buff.type_
                if expected_type == "select_type": # warning : not  tested because not sure we should rely to this select_type keyword
                    expected_type="select"
                elif expected_type == "select_case": # warning : not  tested because not sure we should rely to this select_case keyword
                    expected_type="select"
                type_end=items[1]
                if expected_type != type_end:
                    msg = f"Bad end type for END statement  {line_idx1}:{line} (expecting {expected_type})"
                    logger.critical(msg)
                    raise TucanParsingError(msg)

            stack.append(
                new_stack_item(last_buff, line_idx2, stat_idx, line, verbose=verbose)
            )
            path.pop(-1)
            buffer_pile.pop(-1)
            continue

    # Check specific to fortran
    for stack_item in stack:
        short_type = stack_item.type_.split("_")[0].strip()
        if short_type not in stack_item.end_line:
            pathstr = ".".join(path)
            logger.debug(
                f"End mismatch \nat {pathstr} for {short_type}:\n '{stack_item.start_line_idx}' to '{stack_item.end_line_idx}'.\n For {stack_item.type_} in {stack_item.end_line}"
            )

    # if len(ins_) != len(out_):
    #     for aa, bb in zip(ins_, out_):
    #         logger.warning(f"{aa}<>{bb}")
    #     logger.error(
    #         "Missing one structure statement such as end if... removing file from current analysis"
    #     )
    #     return {}

    return struct_from_stack(stack, main_types=PARTS + ["procedure"])


def _parse_name_ftn(line: str, line_nb: int) -> Tuple[str, str]:
    """expect a lowercase stripped line
    takes the second word as the name
    """

    line = rm_parenthesis_content(line)

    tokens = tokenize(line)
    # no names
    if tokens[0] in NESTS + [
        "interface"
    ]:  # because interface is usually used without name
        name = line.split()[0] + str(line_nb)
        if "#LABEL" in line:
            name += "_" + line.split("#")[-1].split(":")[-1].strip()
    elif "::" in tokens:
        idx = tokens.index("::")
        name = tokens[idx + 1]
    else:
        name = tokens[1]

    type_ = tokens[0]

    return name, type_


##### FTN specific functions


def find_callables_ftn(tokenized_code: List[list]) -> list:
    """Find callables in fortran"""
    candidates = []
    for tokens in tokenized_code:
        if "call" in tokens:
            candidates.append(tokens[tokens.index("call")+1])
        else:
            candidates.extend(find_words_before_left_parenthesis_noregexp(tokens))
    # NB we expect lines like 'call mysubroutine()' to be caught by left parenthesis law$
    matches = [
        cand.replace("%", ".")
        for cand in set(candidates)
        if cand
        not in INTRINSICS
        + [
            "__type_is__",
            "__type_from__",
            "select_type",
            "double_precision",
            "if",
            ".or.",
            ".and.",
        ]
    ]

    return sorted(matches)  # Must be sorted for testing


def build_ftn_ctrl_points(code: List[list])-> list:
    """build the nested list of control points"""
    listpath=[]
    root_path=[]
    increment_control_pts = ["if"]
    constant_control_pts = ["case", "else"]
    
    for tokens_line in code:
        if not tokens_line: #empty line
            continue
        if tokens_line[0] in increment_control_pts:
            listpath.append(root_path+[tokens_line[0]])
            root_path.append(tokens_line[0])

        if tokens_line[0] in constant_control_pts:
            listpath.append(root_path+[tokens_line[0]])
            #root_path.append(tokens_line[0])
            
        if tokens_line[0] == "end":
            try:
                if tokens_line[1] in increment_control_pts:
                    try:
                        root_path.pop(-1)
                    except IndexError:
                        msg_err="Error while building controlpoints."
                        logger.warning(msg_err)
                        raise TucanCtrlPtsError(msg_err)
                    
            except IndexError:
                pass
    

    ctrl_points = [[]]
    for path in listpath:
        inserter=ctrl_points
        for _ in path:
            inserter=inserter[-1]
        inserter.extend([path[-1],[]])

    ctrl_points=ctrl_points[0]

        
    return ctrl_points


def compute_complexities_ftn(indents_code: List[int], tokenized_code: List[list]) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    avg_indent = sum(indents_code)/len(indents_code)/2
    ctrls_pts = build_ftn_ctrl_points(tokenized_code)
    mccabe = compute_cyclomatic_complexity(ctrls_pts)
    possible_paths = compute_possible_paths(ctrls_pts)
    volume, difficulty, effort =  halstead_properties(*halstead_numbers(tokenized_code, PARTS+NESTS+INTRINSICS))
    time_to_code = int(effort/18)

    return round(avg_indent,2),mccabe,possible_paths,volume, difficulty,time_to_code


def compute_cst_ftn(type_: str) -> int:
    """State the structural complexity of a code

    in Short, the average nb. of time we re-read the element.
    It does NOT means it's bad practice
    It just means more read time for the reader to understand the code"""

    cst_ = {
        "program": 0,
        "module": 1,
        "function": 1,
        "subroutine": 2,
        "interface": 4,
        "procedure": 4,
        "type": 6,
    }
    if type_ not in cst_:
        logger.warning(f"Type {type_} not present in conversion list ")
        return 1

    return cst_.get(type_, 1)
