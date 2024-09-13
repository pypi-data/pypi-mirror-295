import sys
from loguru import logger

def startlog(verbose: bool):
    """General logging function of PACKAGE

    """
    format_verbose = "<level>{level}</level> - <blue>{file}:{function}:{line}</blue> - <level>{message}</level>"
    format_normal = "<level>{message}</level>"
    logger.remove()    
    if verbose:
        logger.add(sys.stdout, format=format_verbose,level="TRACE",backtrace=True,diagnose=True)
    else:
        logger.add(sys.stdout, format=format_normal, level="INFO",backtrace= False)
        
    