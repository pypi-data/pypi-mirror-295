import enum

import llvmpym_ext


class Binary(llvmpym_ext.PyBinaryObject):
    """Binary"""

    def __init__(self, mem_buf: llvmpym_ext.core.MemoryBuffer, context: llvmpym_ext.core.Context | None) -> None:
        """
        Create a binary file from the given memory buffer.
        The exact type of the binary file will be inferred automatically, and theappropriate implementation selected.  The context may be NULL except ifthe resulting file is an LLVM IR file.
        """

    @property
    def memory_buffer(self) -> llvmpym_ext.core.MemoryBuffer:
        """
        Retrieves a copy of the memory buffer associated with this object file.

        The returned buffer is merely a shallow copy and does not own the actualbacking buffer of the binary.
        """

    @property
    def type(self) -> BinaryType:
        """Retrieve the specific type of a binary."""

class BinaryType(enum.Enum):
    """BinaryType"""

    LLVMBinaryTypeArchive = 0
    """Archive file."""

    LLVMBinaryTypeMachOUniversalBinary = 1
    """Mach-O Universal Binary file."""

    LLVMBinaryTypeCOFFImportFile = 2
    """COFF Import file."""

    LLVMBinaryTypeIR = 3
    """LLVM IR."""

    LLVMBinaryTypeWinRes = 4
    """Windows resource (.res) file."""

    LLVMBinaryTypeCOFF = 5
    """COFF Object file."""

    LLVMBinaryTypeELF32L = 6
    """ELF 32-bit, little endian."""

    LLVMBinaryTypeELF32B = 7
    """ELF 32-bit, big endian."""

    LLVMBinaryTypeELF64L = 8
    """ELF 64-bit, little endian."""

    LLVMBinaryTypeELF64B = 9
    """ELF 64-bit, big endian."""

    LLVMBinaryTypeMachO32L = 10
    """MachO 32-bit, little endian."""

    LLVMBinaryTypeMachO32B = 11
    """MachO 32-bit, big endian."""

    LLVMBinaryTypeMachO64L = 12
    """MachO 64-bit, little endian."""

    LLVMBinaryTypeMachO64B = 13
    """MachO 64-bit, big endian."""

    LLVMBinaryTypeWasm = 14
    """Web Assembly."""

    LLVMBinaryTypeOffload = 15
    """Offloading fatbinary."""
