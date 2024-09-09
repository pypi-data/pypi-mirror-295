from collections.abc import Sequence
import types
from typing import Any


def add_symbol(symbol_name: str, symbol_value: Any) -> None:
    """
    This functions permanently adds the symbol symbolName with thevalue symbolValue.  These symbols are searched before anylibraries.
    """

def load_library_permanently(filename: str) -> bool:
    """
    This function permanently loads the dynamic library at the given path.It is safe to call this function multiple times for the same library.
    """

def parse_command_line_options(args: Sequence[str], overview: str) -> None:
    """
    This function parses the given arguments using the LLVM command line parser.Note that the only stable thing about this function is its signature; youcannot rely on any particular set of command line arguments being interpretedthe same way across LLVM versions.
    """

def search_for_address_of_symbol(name: str) -> types.CapsuleType:
    """
    This function will search through all previously loaded dynamiclibraries for the symbol symbolName. If it is found, the address ofthat symbol is returned. If not, null is returned.
    """
