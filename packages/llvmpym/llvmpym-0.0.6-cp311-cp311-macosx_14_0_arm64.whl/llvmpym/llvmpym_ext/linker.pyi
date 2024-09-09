import enum

import llvmpym_ext


class LinkerModeLinkerMode(enum.Enum):
    DestroySource = 0
    """This is the default behavior."""

def link_module(dest: llvmpym_ext.core.Module, src: llvmpym_ext.core.Module) -> bool:
    """
    Links the source module into the destination module. The source module isdestroyed.
    The return value is true if an error occurred, false otherwise.
    Use the diagnostic handler to get any diagnostic message.
    """
