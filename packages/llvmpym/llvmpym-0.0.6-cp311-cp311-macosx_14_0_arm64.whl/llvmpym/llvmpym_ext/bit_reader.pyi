import llvmpym_ext


def get_bitcode_module(mem_buf: llvmpym_ext.core.MemoryBuffer) -> llvmpym_ext.core.Module: ...

def parse_bit_code(mem_buf: llvmpym_ext.core.MemoryBuffer) -> llvmpym_ext.core.Module:
    """
    Builds a module from the bitcode in the specified memory buffer, returning areference to the module via the OutModule parameter.
    """
