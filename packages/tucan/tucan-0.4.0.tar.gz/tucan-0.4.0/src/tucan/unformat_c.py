from typing import List
from loguru import logger

from tucan.unformat_common import (
    Statements,
    new_stmts,
    remove_strings,
    clean_blanks,
    clean_inline_comments,
    rm_parenthesis_content,
    align_multiline_blocks,
    align_end_continuations,
)

from tucan.string_utils import eat_spaces, get_indent, tokenize

from tucan.kw_lang import KEYWORDS_C


# TODO remove all spaces and reformat?
def remove_space_in_front_of_variables(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stmts (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line
        for keyword in KEYWORDS_C:
            if keyword in line.split() and "=" in line:
                if line.split()[1] == "=":
                    stmt = line.replace(line.split()[0] + " =", line.split()[0] + "=")
                    logger.warning(
                        f"A C Keywords {keyword} is used as a variable in the code. Bad Practice Should Be Avoided"
                    )
                continue
            continue

        new_stmt.append(stmt)
        new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)


def split_blocks(stmts: Statements) -> Statements:
    """Split statements on { and } markers"""
    new_stmt = []
    new_lines = []
    stmt = ""
    level = 0
    INDENT = "  "
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        # skip void lines
        if line.strip() == "":
            continue

        # exception for includes
        if line.startswith("#"):
            new_stmt.append(line)
            new_lines.append([lstart, lend])
            continue

        for char in line:
            if char in ["{"]:
                if stmt.strip() == "":  # edge case, line directly starts with {
                    new_stmt[-1] += (
                        " " + char
                    )  # we add this char to the previous statement
                    new_lines[-1][
                        -1
                    ] = lend  # and update the endline of prev statement  (ONLY CASE Where linespan changes)
                else:
                    new_stmt.append(
                        level * INDENT + stmt.lstrip() + char
                    )  # normal case , we add the statement with the char
                    new_lines.append([lstart, lend])  # and the lines spa
                level += 1  # lvl is increased
                stmt = ""  # stmt is reset
            elif char in ["}"]:
                if stmt.strip() != "":  # edge case, line directly starts with }
                    new_stmt.append(
                        level * INDENT + stmt.lstrip()
                    )  # we add the last statement  wo the "}"
                    new_lines.append([lstart, lend])  # same line span
                level -= 1  # lvl is increased
                new_stmt.append(
                    level * INDENT + char
                )  # a new statement is added with "}"
                new_lines.append([lstart, lend])  # same line span
                stmt = ""  # stmt is reset
            elif (
                char in [";"]
                and new_stmt
                and new_stmt[-1][-1] in ["}"]
                and stmt.strip() == ""
            ):
                continue  # if a ; follows directly a }
            else:
                stmt += char

        # line is finished. If statmt is not void, add sttment
        if stmt.strip() != "":
            new_stmt.append(level * INDENT + stmt.lstrip())
            new_lines.append([lstart, lend])
            stmt = ""

    return Statements(new_stmt, new_lines)


def merge_lines_by_end(stmts: Statements) -> Statements:
    """Ensure lines only ends with {,},;,:"""
    new_stmt = []
    new_lines = []
    stmt = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if stmt == "":
            tmp_start = lstart
            stmt = get_indent(line)
        else:
            stmt += " "

        stmt += line.lstrip()

        if line.startswith("#"):
            new_stmt.append(stmt)
            new_lines.append([tmp_start, lend])
            stmt = ""
            continue

        if line.endswith(("{", ";", ":", "}")) or lend == stmts.lines[-1][-1]:
            new_stmt.append(stmt)
            new_lines.append([tmp_start, lend])
            stmt = ""

    return Statements(new_stmt, new_lines)


def merge_parenthesis_lines(stmts: Statements) -> Statements:
    new_stmt = []
    new_lines = []
    stmt = ""
    lvl = 0
    istart = 0
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if lvl > 0:
            line = " " + line.lstrip()
        else:
            istart = lstart

        for char in line:
            if char in ["("]:
                lvl += 1
            if char in [")"]:
                lvl -= 1
            stmt += char

        if lvl == 0:
            new_stmt.append(stmt)
            new_lines.append([istart, lend])
            stmt = ""

    return Statements(new_stmt, new_lines)


# def split_multiple_statements(stmts: Statements) -> Statements:
#     """Split lines with multiples ; """
#     new_stmt = []
#     new_lines = []
#     for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
#         if line.lstrip().startswith("for "):
#             new_stmt.append(line)
#             new_lines.append([lstart, lend])
#             continue

#         stmt = line.rstrip(";").rstrip()
#         indent=get_indent(line)
#         for item in stmt.split(";"):
#             new_stmt.append(indent+item.strip()+";")
#             new_lines.append([lstart, lend])

#     return Statements(new_stmt, new_lines)


# def split_declarations(stmts: Statements) -> Statements:
# """Split functions declarations, to make clean signatures """
# new_stmt = []
# new_lines = []
# tail = " ###==============================="
# def _need_split(buffer:str)->bool:
# try:
# cleanstr = rm_parenthesis_content(buffer[:-1])
# type_,name_ = cleanstr.lstrip().split()
# if "=" not in name_:
# return True
# except ValueError:
# pass
# return False


# for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
# buffer=""
# for char in line:
# buffer+=char
# if char == "{":
# if _need_split(buffer):
# new_stmt.append(buffer+tail)
# new_lines.append([lstart, lend])
# buffer=get_indent(line)+"    "
# if char == "}":
# pass
# new_stmt.append(buffer)
# new_lines.append([lstart, lend])
# return Statements(new_stmt, new_lines)


def line_to_flag(line, iline):
    """Check if line should be flagged"""
    # obvious fallbacks

    tokens = tokenize(line)

    if tokens[0] in ["template"]:
        return True

    if not tokens[-1] in ["{"]:
        return False

    if tokens[0] in ["if", "case", "else", "switch", "enum", "return"]:
        return False

    if "=" in tokens:
        return False

    if len(tokens) <= 2:
        return False

    #    if not tokens[1].isalnum():
    #        return False

    #   logger.critical(tokens)

    return True


def flag_declarations(code: List[str]) -> List[str]:
    """Split functions declarations, to make clean signatures"""
    new_lines = []
    tail = " ###==============================="

    for iline, line in enumerate(code):
        new_lines.append(line)
        if line_to_flag(line, iline):
            if line.endswith(";"):
                new_lines[-1] += "{}"
            new_lines[-1] += tail

    return new_lines


def unformat_c(code: List[str]) -> Statements:
    """
    Unformat C code by stripping comments and moving leading '&' characters.

    Args:
        code (List[str]): List of C code lines.

    Returns:
        List[Tuple[str, Tuple[int, int]]]: List of unformatted code statements along with line number ranges.
    """
    stmts = new_stmts(code)
    stmts.stmt = eat_spaces(stmts.stmt)
    stmts.stmt = remove_strings(stmts.stmt, '"')
    stmts.stmt = remove_strings(stmts.stmt, "'")
    stmts = align_multiline_blocks(stmts, "/*", "*/")
    stmts = clean_inline_comments(
        stmts, "/*"
    )  # this ine must follow the align multiline block
    stmts = clean_inline_comments(stmts, "//")
    stmts = clean_blanks(
        stmts
    )  # this one must follow the clean inline, to remove blank lines
    stmts = align_end_continuations(stmts, "\\")
    stmts = split_blocks(stmts)
    stmts = merge_parenthesis_lines(stmts)
    stmts = merge_lines_by_end(stmts)
    stmts.stmt = flag_declarations(stmts.stmt)

    # stmts = remove_space_in_front_of_variables(stmts)

    return stmts
