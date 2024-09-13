from loguru import logger
from typing import List

TOKEN_CUT = {
    ("alphanum", "alphanum"): False,  # word
    ("alphanum", "space"): True,  # end of word
    ("alphanum", "dot"): False,  # dotsep
    ("alphanum", "other"): True,  # end of word
    ("space", "alphanum"): True,  # word
    ("space", "space"): None,  # end of word
    ("space", "dot"): True,  # number
    ("space", "other"): True,  # end of word
    ("dot", "alphanum"): False,  # word
    ("dot", "space"): True,  # end of word
    ("dot", "dot"): False,  # number
    ("dot", "other"): True,  # end of word
    ("other", "alphanum"): True,  # word
    ("other", "space"): True,  # end of word
    ("other", "dot"): True,  # number
    ("other", "other"): True,  # end of word
}

META_CHARS = {
    ".eq.": "\xaa",  # comparison
    ".neq.": "\xab",
    ".ge.": "\xac",
    ".gt.": "\xad",
    ".le.": "\xae",
    ".lt.": "\xaf",
    ".and.": "\xba",  # logic
    ".or.": "\xbb",
    "//": "\xca",  # markers
    "/*": "\xcb",
    "*/": "\xcc",
    "::": "\xcd",
    "||": "\xce",
    "&&": "\xcf",
    "+=": "\xda",  # operands
    "-=": "\xdb",
    "/=": "\xdc",
    "*=": "\xdd",
    "**": "\xde",
    "==": "\xdf",
    ">=": "\xea",  # operands
    "<=": "\xeb",
    "<<": "\xec",
}

META_CHARS_REV = {value: key for key, value in META_CHARS.items()}

STRING_START = "\xfa"
STRING_STOP = "\xfb"
STRING_SUB = "\xfc"

STR_SUBSTITUTE = {
    "\xfa": '"',
    "\xfb": '"',
    "\xfc": "'",
}


# def string_encode(line: str) -> str:
#     string_type = ""
#     new_line = ""
#     for char in line:
#         if char in ["'", '"']:
#             if string_type == "":  # <- Enter string
#                 new_line += STRING_START
#                 string_type = char
#             else:  # in a string
#                 if char == string_type:
#                     new_line += STRING_STOP
#                     string_type = ""
#                 else:
#                     new_line += STRING_SUB
#         else:
#             new_line += char
#     assert len(new_line) == len(line)
#     return new_line

def string_encode(line: str) -> str:
    string_type = ""
    result = []
    for char in line:
        if char in ["'", '"']:
            if not string_type:  # Enter string
                result.append(STRING_START)
                string_type = char
            elif char == string_type:  # Close string
                result.append(STRING_STOP)
                string_type = ""
            else:  # Different string character within string
                result.append(STRING_SUB)
        else:
            result.append(char)
    return ''.join(result)

# def string_decode(line: str) -> str:
#     new_line = ""
#     for char in line:
#         new_line += STR_SUBSTITUTE.get(char, char)
#     return new_line

def string_decode(line: str) -> str:
    return ''.join(STR_SUBSTITUTE.get(char, char) for char in line)


def metachar_encode(line: str) -> str:
    for char, proxy in META_CHARS.items():
        line = line.replace(char, proxy)
    return string_encode(line)


# def metachar_encode(line: str) -> str:
#     # cannot work, its not by single char
#     return string_encode(''.join(META_CHARS.get(char, char) for char in line))


# def metachar_decode(line: str) -> str:
#     for char, proxy in META_CHARS.items():
#         line = line.replace(proxy, char)
#     return string_decode(line)

# def metachar_decode(line: str) -> str:
#     result = line
#     for char, proxy in META_CHARS.items():
#         result = result.replace(proxy, char)
#     return string_decode(result)


def metachar_decode(line: str) -> str:
    return string_decode(''.join(META_CHARS_REV.get(char, char) for char in line))



# def metachar_decode_from_list(list_: str) -> List:
#     # logger.critical(list_)
#     # list_ = [  META_CHARS_REV.get(item, item) for item in list_]
#     list_ = [metachar_decode(item) for item in list_]

#     # logger.critical(list_)
#     list_ = [string_decode(item) for item in list_]
#     # logger.critical(list_)
#     return list_

def metachar_decode_from_list(list_: List[str]) -> List[str]:
    return [string_decode(metachar_decode(item)) for item in list_]

def iterate_with_neighbors(iterable_):
    # Create iterators for the current and previous characters
    prev = None  # Initialize previous character to None
    for curr in iterable_:
        # Yield the previous and current characters
        yield prev, curr
        prev = curr
    yield prev, None


def tokenize(line: str) -> List[str]:
    """
    Light tokenizer to ease code identification
    """

    def _cast(char):
        if char == " ":
            return "space"
        if char in [".", "_", "%", "\xcd"]:  # \xcd is the :: marker
            return "dot"
        if char in META_CHARS_REV.keys():
            return "other"
        if char.isalnum():
            return "alphanum"
        return "other"

    tokens = []
    buffer = ""
    prev_cast = "other"
    instring = False
    for curr_char in metachar_encode(line):
        cur_cast = _cast(curr_char)
        to_cut = TOKEN_CUT[prev_cast, cur_cast]

        # string override; a string is a single token
        if curr_char == STRING_START:
                instring = True
                if buffer.strip() != "":
                    tokens.append(buffer)
                buffer = ""
        if curr_char == STRING_STOP:
            if buffer.strip() != "":
                buffer += curr_char
                tokens.append(buffer)
            buffer = ""
            instring = False
            continue

        if instring:
            buffer += curr_char
            continue
        # string override; a string is a single token

        if to_cut is None:
            continue
        elif to_cut is True:
            if buffer.strip() != "":
                tokens.append(buffer)
            buffer = curr_char
        else:
            buffer += curr_char

        prev_cast = cur_cast

    if buffer.strip() != "":
        tokens.append(buffer)

    return metachar_decode_from_list(tokens)


def find_words_before_left_parenthesis_noregexp(tokens: List[str]) -> List[str]:
    """Find all words before a left parenthesis in a line"""
    if "(" not in tokens:
        return []
    matches = []
    for prev, curr in iterate_with_neighbors(tokens):
        if curr == "(":
            try:
                if prev not in ",+-/*<>=;|(){}[]:&!~ ":
                    matches.append(prev)
            except TypeError:
                pass  # triggered by prev == None

    clean_matches = sorted(set(matches))

    black_list = list(META_CHARS.keys()) + ["!"]
    # remove meta chars , whit ar not words...
    clean_matches = [item for item in clean_matches if item not in black_list]

    return clean_matches


def get_indent(line: str) -> str:
    """Get the indentation leading a line"""
    _indent = ""
    for char in line:
        if char == "\t":
            _indent += "    "
        elif char != " ":
            return _indent
        else:
            _indent += " "
    return _indent


def average_indent(code:List[str])->float:
    """Average indentation lvl of code"""
    sum=0
    for line in code:
        sum+=len(get_indent(line))
    return 1.*sum / len(code)


def eat_spaces(code: List[str]) -> List[str]:
    """Remove unwanted multiple spacing"""
    new_stmt = []
    for line in code:
        line = line.replace("\t","  ") 
        out = get_indent(line)

        prevchar = None
        for i, char in enumerate(line.strip()):
            try:
                next_char = line.strip()[i + 1]
            except IndexError:
                next_char = None

            if char == " ":
                if prevchar not in [" ", ":", ";", ","] and next_char not in [
                    ":",
                    ";",
                    ",",
                ]:
                    out += char
                else:
                    pass  # no space needed if " " precedes, or a punctuation is before or after
            else:
                out += char

            prevchar = char
        new_stmt.append(out)
    return new_stmt


def get_common_root_index(list_:list)-> int:
    "return the index of the first character differing after a common root"
    if "" in list_:
        return 0


    def root_ok_str(list_:list, root):
        """ 
        - list_ is a list of str and root is a string
        - list_ is a list of list of str and root is a list of str
        
        """
        for item_ in list_:
            if not item_.startswith(root) :
                return False
        return True
    

    one_ = list_[0]
    idx = 0
    while root_ok_str(list_, one_[:idx]):# and idx<len(list_[0])-1 :
        #logger.info(one_[:idx])
        #logger.info(idx)
        idx+=1
        
    out = idx-2
            
    return out



def get_common_root_index_list(list_:List[List[str]])-> int:
    "return the index of the first character differing after a common root"
    if [] in list_:
        return 0


    def root_ok_list(list_:list, root):
        """ 
        - list_ is a list of str and root is a string
        - list_ is a list of list of str and root is a list of str
        
        """
        #logger.warning(f"root {root}")
        #logger.warning(f"all items {list_}")
        
        for item_ in list_:
            #logger.warning(f"root {root}, item {item_[0:len(root)]}" )
            if root != item_[0:len(root)] :
                return False
        return True
    

    one_ = list_[0]
    idx = 0
    while root_ok_list(list_, one_[:idx]):
        #logger.info(one_[:idx])
        #logger.info(idx)
        idx+=1
        
    out = idx-2
    #logger.info(out)
            
    return out



def best_front_match(str_ :iter,list_str:List[iter])->iter:
    """
    Return the str in LIST_STR with the longest match w.r. to str_
    generalized to iterables if needed.
    """
    
    #references = [ref for ref in references if ref.startswith(prefix)]
    lmatch =0
    smatch=None
    for candidate in list_str:
        count = front_match(str_,candidate)
        if count > lmatch:
            lmatch =count
            smatch = candidate    
    return smatch

def front_match(list1: iter, list2: iter) -> int:
    """
    Count the number of matching elements from the end of two iterable.

    Args:
        list1 (iterable): The first iterable to compare.
        list2 (iterable): The second iterable to compare.

    Returns:
        int: The number of matching elements from the end of both iterable.
    """
    count = 0

    # Compare elements from the end of the lists
    for elem1, elem2 in zip(list1, list2):
        if elem1 == elem2:
            count += 1
        else:
            break

    return count


def inner_match(list1: iter, list2: iter) -> int:
    """
    Count the number of sequential matching elements between two iterable.

    Args:
        list1 (iterable): The first iterable to compare.
        list2 (iterable): The second iterable to compare.

    Returns:
        int: The number of matching elements from the end of both iterable.
    """
    count = 0

    # Compare elements from the end of the lists
    jstart = None
    for istart, item in enumerate(list1):
        if item in list2:
            jstart=list2.index(item)
            break
    
    if jstart is None:
        #print(f"None of {list1} found in {list2}")
        return 0

    count = 0
    try:
        while list1[istart+count] == list2[jstart+count]:
            count+=1
    except IndexError:
        pass 
    #print(f"Found {count} matchs for {list1} and {list2}")
    return count

def best_inner_match(str_ :iter,list_str:List[iter])->list:
    """
    Return the str in LIST_STR with the longest match w.r. to str_
    generalized to iterables if needed.
    """
    
    #references = [ref for ref in references if ref.startswith(prefix)]
    lmatch =0
    imatch=[]
    for i,candidate in enumerate(list_str):
        count = inner_match(str_,candidate)
        #logger.info(f"Found {count} matchs for {str_} in {candidate}")
        if count == 0:
            continue
        if count > lmatch:
            lmatch =count
            imatch=[i]
        elif count == lmatch:
            imatch.append(i)  
    return imatch


def generate_dict_paths(d:dict, path:list=None)-> list:
    if path is None:
        path = []

    if isinstance(d, dict) and d != {} :
        paths = []
        for k, v in d.items():
            new_path = path + [k]
            paths.extend(generate_dict_paths(v, new_path))
        return paths
    else:
        return [path]

