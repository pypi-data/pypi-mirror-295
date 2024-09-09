import enum

import llvmpym_ext


class VerifierFailureAction(enum.Enum):
    """VerifierFailureAction"""

    AbortProcess = 0
    """verifier will print to stderr and abort()"""

    PrintMessage = 1
    """verifier will print to stderr and return 1"""

    ReturnStatus = 2
    """verifier will just return 1"""

def view_function_cfg(fn: llvmpym_ext.core.Function) -> None:
    """
    Open up a ghostview window that displays the CFG of the current function. Useful for debugging.
    """

def view_function_cfg_only(fn: llvmpym_ext.core.Function) -> None:
    """
    Open up a ghostview window that displays the CFG of the current function. Useful for debugging.
    """
