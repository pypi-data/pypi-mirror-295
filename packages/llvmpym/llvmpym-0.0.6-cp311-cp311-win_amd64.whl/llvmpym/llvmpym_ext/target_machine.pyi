import enum
from typing import overload

import llvmpym_ext


class CodeGenOptLevel(enum.Enum):
    """CodeGenOptLevel"""

    Null = 0

    Less = 1

    Default = 2

    Aggressive = 3

class CodeModel(enum.Enum):
    """CodeModel"""

    Default = 0

    JITDefault = 1

    Tiny = 2

    Small = 3

    Kernel = 4

    Medium = 5

    Large = 6

class RelocMode(enum.Enum):
    """RelocMode"""

    Default = 0

    Static = 1

    PIC = 2

    DynamicNoPic = 3

    ROPI = 4

    RWPI = 5

    ROPI_RWPI = 6

class Target(llvmpym_ext.PymTargetObject):
    """Target"""

    def __iter__(self) -> TargetIterator: ...

    @staticmethod
    def get_first() -> Target:
        """Returns the first llvm::Target in the registered targets list."""

    @staticmethod
    def get_from_name(name: str) -> Target:
        """Finds the target corresponding to the given name"""

    @staticmethod
    def get_from_triple(triple: str) -> Target:
        """
        Finds the target corresponding to the given triple.Raises:
        	RuntimeError
        """

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def has_jit(self) -> bool: ...

    @property
    def has_target_machine(self) -> bool: ...

    @property
    def has_asm_backend(self) -> bool: ...

    @property
    def next(self) -> Target | None:
        """
        Returns the next llvm::Target given a previous one (or null if there's none)
        """

class TargetIterator:
    """TargetIterator"""

    def __iter__(self) -> TargetIterator: ...

    def __next__(self) -> Target: ...

class TargetMachine(llvmpym_ext.PymTargetMachineObject):
    """TargetMachine"""

    @overload
    def __init__(self, target: Target, triple: str, options: TargetMachineOptions) -> None: ...

    @overload
    def __init__(self, arg0: Target, arg1: str, arg2: str, arg3: str, arg4: CodeGenOptLevel, arg5: RelocMode, arg6: CodeModel, /) -> None: ...

    @property
    def target(self) -> Target: ...

    @property
    def triple(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

    @property
    def cpu(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

    @property
    def feature_string(self) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

    @property
    def data_layout(self) -> "PymTargetData": ...

    def set_asm_verbosity(self, verbose: bool) -> None: ...

    def set_fast_isel(self, enable: bool) -> None: ...

    def set_global_isel(self, enable: bool) -> None: ...

    def set_global_isel_abort(self, mode: "LLVMGlobalISelAbortMode") -> None: ...

    def set_machine_outliner(self, enable: bool) -> None: ...

    def emit_to_file(self, module: llvmpym_ext.core.Module, filename: str, codegen: "LLVMCodeGenFileType") -> None:
        """
        Emits an asm or object file for the given module to the filename. Thiswraps several c++ only classes (among them a file stream).

        Raises:
        	RuntimeError
        """

    def emit_to_memory_buffer(self, module: llvmpym_ext.core.Module, codegen: "LLVMCodeGenFileType") -> None: ...

    def add_analysis_passes(self, pm: llvmpym_ext.core.PassManager) -> None:
        """Adds the target-specific analysis passes to the pass manager."""

class TargetMachineOptions(llvmpym_ext.PymTargetMachineOptionsObject):
    """TargetMachineOptions"""

    def __init__(self) -> None: ...

    def set_cpu(self, cpu: str) -> None: ...

    def set_features(self, features: str) -> None: ...

    def set_abi(self, abi: str) -> None: ...

    def set_code_gen_opt_level(self, level: CodeGenOptLevel) -> None: ...

    def set_reloc_mode(self, reloc: RelocMode) -> None: ...

    def set_code_model(self, code_model: CodeModel) -> None: ...

def get_default_target_triple() -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

def get_host_cpu_features() -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

def get_host_cpu_name() -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...

def normalize_target_triple(arg: str, /) -> "std::basic_string<char,std::char_traits<char>,std::allocator<char> >": ...
