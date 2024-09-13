"""Custom tucan exeptions"""


class TucanError(RuntimeError):
    """General tucan error
    
    If you are coming from another package, use this by default """
    pass

class TucanParsingError(TucanError):
    """raised is tucan reach a known potential dead en in parsing code
    
    e.g. reaching an fortran end statement withoud corresponding context"""
    pass

class TucanCtrlPtsError(TucanError):
    """raised is tucan reach a dead end when building the control points
    
    e.g. interpreting python code with spurious indentations"""
    pass