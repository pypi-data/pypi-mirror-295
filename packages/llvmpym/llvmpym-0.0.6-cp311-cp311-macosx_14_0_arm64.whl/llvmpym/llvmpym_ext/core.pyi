from collections.abc import Callable, Sequence
import enum
import types
from typing import Any, overload

import llvmpym_ext


AllFMFlag: int = 127

class AllocaInst(Instruction):
    """AllocaInst"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def type(self) -> Type: ...

AllowContractFMFlag: int = 32

AllowReassocFMFlag: int = 1

AllowReciprocalFMFlag: int = 16

ApproxFuncFMFlag: int = 64

class Argument(Value):
    """Argument"""

    def __repr__(self) -> str: ...

    @property
    def parent(self) -> Function:
        """Obtain the function to which this argument belongs."""

    @property
    def next(self) -> Argument | None: ...

    @property
    def prev(self) -> Argument | None: ...

    @property
    def attrs(self) -> list[Attribute]: ...

    def set_alignment(self, arg: int, /) -> None: ...

class ArrayType(SequenceType):
    """ArrayType"""

    def __init__(self, elem_type: Type, elem_count: int) -> None:
        """
        Create a fixed size array type that refers to a specific type.

        The created type will exist in the context that its element typeexists in.
        """

    def __repr__(self) -> str: ...

    @property
    def length(self) -> int: ...

class AtomicCmpXchgInst(Instruction):
    """AtomicCmpXchgInst"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def is_volatile(self) -> bool: ...

    @is_volatile.setter
    def is_volatile(self, arg: bool, /) -> None: ...

    @property
    def is_weak(self) -> int: ...

    @is_weak.setter
    def is_weak(self, arg: bool, /) -> None: ...

    @property
    def is_single_thread(self) -> bool: ...

    @is_single_thread.setter
    def is_single_thread(self, arg: bool, /) -> None: ...

    @property
    def success_ordering(self) -> AtomicOrdering: ...

    @success_ordering.setter
    def success_ordering(self, arg: AtomicOrdering, /) -> None: ...

    @property
    def failure_ordering(self) -> AtomicOrdering: ...

    @failure_ordering.setter
    def failure_ordering(self, arg: AtomicOrdering, /) -> None: ...

class AtomicOrdering(enum.Enum):
    """AtomicOrdering"""

    NotAtomic = 0
    """A load or store which is not atomic"""

    Unordered = 1
    """
    Lowest level of atomicity, guarantees somewhat sane results, lock free.
    """

    Monotonic = 2
    """
    guarantees that if you take all the operations affecting a specific address, a consistent ordering exists
    """

    Acquire = 4
    """
    Acquire provides a barrier of the sort necessary to acquire a lock to access other memory with normal loads and stores.
    """

    Release = 5
    """
    Release is similar to Acquire, but with a barrier of the sort necessary to release a lock.
    """

    AcquireRelease = 6
    """
    provides both an Acquire and a Release barrier (for fences and operations which both read and write memory).
    """

    SequentiallyConsistent = 7
    """
    provides Acquire semantics for loads and Release semantics for stores. Additionally, it guarantees that a total ordering exists between all SequentiallyConsistent operations.
    """

class AtomicRMWBinOp(enum.Enum):
    """AtomicRMWBinOp"""

    Xchg = 0
    """Set the new value and return the one old"""

    Add = 1
    """Add a value and return the old one"""

    Sub = 2
    """Subtract a value and return the old one"""

    And = 3
    """And a value and return the old one"""

    Nand = 4
    """Not-And a value and return the old one"""

    Or = 5
    """OR a value and return the old one"""

    Xor = 6
    """Xor a value and return the old one"""

    Max = 7
    """
    Sets the value if it's greater than the original using a signed comparison and return the old one
    """

    Min = 8
    """
    Sets the value if it's Smaller than the original using a signed comparison and return the old one
    """

    UMax = 9
    """
    Sets the value if it's greater than the original using an unsigned comparison and return the old one
    """

    UMin = 10
    """
    Sets the value if it's greater than the original using an unsigned comparison and return the old one
    """

    FAdd = 11
    """Add a floating point value and return the old one"""

    FSub = 12
    """Subtract a floating point value and return the old one"""

    FMax = 13
    """
    Sets the value if it's greater than the original using an floating point comparison and return the old one
    """

    FMin = 14
    """
    Sets the value if it's smaller than the original using an floating point comparison and return the old one
    """

class AtomicRMWInst(Instruction):
    """AtomicRMWInst"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def is_volatile(self) -> bool: ...

    @is_volatile.setter
    def is_volatile(self, arg: bool, /) -> None: ...

    @property
    def ordering(self) -> AtomicOrdering: ...

    @ordering.setter
    def ordering(self, arg: AtomicOrdering, /) -> None: ...

    @property
    def bin_op(self) -> AtomicRMWBinOp: ...

    @bin_op.setter
    def bin_op(self, arg: AtomicRMWBinOp, /) -> None: ...

    @property
    def is_single_thread(self) -> bool: ...

    @is_single_thread.setter
    def is_single_thread(self, arg: bool, /) -> None: ...

class Attribute(llvmpym_ext.PymAttributeObject):
    """Attribute"""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    @property
    def is_enum(self) -> bool: ...

    @property
    def is_string(self) -> bool: ...

    @property
    def is_type(self) -> bool: ...

class BasicBlock(llvmpym_ext.PymBasicBlockObject):
    """BasicBlock"""

    @overload
    def __init__(self, context: Context, name: str = '') -> None:
        """Create a new basic block without inserting it into a function."""

    @overload
    def __init__(self, context: Context, function: Function, name: str = '') -> None:
        """Create a new basic block without inserting it into a function."""

    @overload
    def __init__(self, context: Context, bb: BasicBlock, name: str = '') -> None:
        """
        Insert a basic block in a function before another basic block.

        The function to add to is determined by the function of thepassed basic block.
        """

    @overload
    def __init__(self, insert_before_bb: BasicBlock, name: str = '') -> None:
        """Insert a basic block in a function using the global context."""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    @property
    def name(self) -> str: ...

    @property
    def parent(self) -> Function:
        """Obtain the function to which a basic block belongs."""

    @property
    def terminator(self) -> Instruction | None:
        """
        Obtain the terminator instruction for a basic block.

        If the basic block does not have a terminator (it is not well-formedif it doesn't), then NULL is returned.
        """

    @property
    def value(self) -> BasicBlockValue: ...

    @property
    def next(self) -> BasicBlock | None: ...

    @property
    def prev(self) -> BasicBlock | None: ...

    @property
    def first_instruction(self) -> Instruction | None: ...

    @property
    def last_instruction(self) -> Instruction | None: ...

    @property
    def instructions(self) -> InstructionIterator: ...

    def create_and_insert_before(self, arg: str, /) -> BasicBlock:
        """Insert a basic block in a function using the global context."""

    def destroy(self) -> None:
        """
        Remove a basic block from a function and delete it.

        This deletes the basic block from its containing function and deletesthe basic block itself.
        """

    def remove_from_parent(self) -> None:
        """
        Remove a basic block from a function.

        This deletes the basic block from its containing function but keepthe basic block alive.
        """

    def move_before(self, pos: BasicBlock) -> None:
        """Move a basic block to before another one."""

    def move_after(self, arg: BasicBlock, /) -> None:
        """Move a basic block to after another one."""

class BasicBlockValue(Value):
    """BasicBlockValue"""

class BranchInst(Instruction):
    """BranchInst"""

    @property
    def is_conditional(self) -> int: ...

    @property
    def condition(self) -> Value: ...

    @condition.setter
    def condition(self, arg: Value, /) -> None: ...

class Builder(llvmpym_ext.PymBuilderObject):
    """Builder"""

    @overload
    def __init__(self, arg: Context, /) -> None: ...

    @overload
    def __init__(self) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def insert_block(self) -> BasicBlock: ...

    @property
    def current_debug_location(self) -> Metadata: ...

    @current_debug_location.setter
    def current_debug_location(self, arg: Metadata, /) -> None: ...

    @property
    def default_fp_math_tag(self) -> Metadata:
        """Get the dafult floating-point math metadata."""

    @default_fp_math_tag.setter
    def default_fp_math_tag(self, arg: Metadata, /) -> None: ...

    def position(self, arg0: BasicBlock, arg1: Instruction, /) -> None:
        """Original Function: LLVMPositionBuilder."""

    def position_before(self, instruction: Instruction) -> None:
        """Original function: LLVMPositionBuilderBefore."""

    def position_at_end(self, basicblock: BasicBlock) -> None:
        """Original function: LLVMPositionBuilderAtEnd."""

    def clear_insert_position(self) -> None: ...

    @overload
    def insert(self, basic_block: BasicBlock) -> None:
        """
        Insert the given basic block after the insertion point of the given builder.

        The insertion point must be valid.
        """

    @overload
    def insert(self, instruction: Instruction) -> None: ...

    def insert_with_name(self, instruction: Instruction, name: str = '') -> None: ...

    def destory(self) -> None:
        """Original Function: LLVMDisposeBuilder."""

    def set_instruction_debug_location(self, instruction: Instruction) -> None:
        """
        Attempts to set the debug location for the given instruction using thecurrent debug location for the given builder.  If the builder has no currentdebug location, this function is a no-op.
        """

    def add_metadata_to_instruction(self, instruction: Instruction) -> None:
        """
        Adds the metadata registered with the given builder to the giveninstruction.
        """

    def ret_void(self) -> ReturnInst: ...

    def ret(self, value: Value) -> ReturnInst: ...

    def aggregate_ret(self, values: Sequence[Value]) -> ReturnInst: ...

    def br(self, dest: BasicBlock) -> BranchInst: ...

    def cond_br(self, If: Value, Then: BasicBlock, Else: BasicBlock) -> BranchInst: ...

    def switch(self, value: Value, Else: BasicBlock, num_cases: int) -> SwitchInst: ...

    def indirect_br(self, addr: Value, num_dests: int) -> IndirectBrInst: ...

    def invoke(self, type: Type, fn: Function, args: Sequence[Value], Then: BasicBlock, Catch: BasicBlock, name: str = '') -> InvokeInst:
        """Original Function: LLVMBuildInvoke2."""

    def invoke_with_operand_bundles(self, type: Type, fn: Function, args: Sequence[Value], Then: BasicBlock, Catch: BasicBlock, bundles: Sequence[OperandBundle], name: str = '') -> InvokeInst: ...

    def unreachable(self) -> Instruction: ...

    def resume(self, exn: Value) -> Instruction: ...

    def landing_pad(self, type: Type, pers_fn: Value, num_clauses: int, name: str = '') -> LandingPadInst: ...

    def cleanup_ret(self, catch_pad: Value, bb: BasicBlock) -> CleanupReturnInst: ...

    def catch_pad(self, parent_pad: Value, args: Sequence[Value], name: str = '') -> CatchPadInst: ...

    def cleanup_pad(self, parent_pad: Value, args: Sequence[Value], name: str = '') -> Instruction: ...

    def catch_switch(self, parent_pad: Value, unwind_bb: BasicBlock, num_handlers: int, name: str = '') -> CatchSwitchInst: ...

    def add(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def add_nsw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def add_nuw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def fadd(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def sub(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def sub_nsw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def sub_nuw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def fsub(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def mul(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def mul_nsw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def mul_nuw(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def fmul(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def udiv(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def exact_udiv(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def sdiv(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def exact_sdiv(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def fdiv(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def urem(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def srem(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def frem(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def shl(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def lshr(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def ashr(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def xor(self, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def binop(self, arg0: Opcode, arg1: Value, arg2: Value, arg3: str, /) -> Value: ...

    def neg(self, arg0: Value, arg1: str, /) -> Value: ...

    def neg_nsw(self, arg0: Value, arg1: str, /) -> Value: ...

    def neg_nuw(self, arg0: Value, arg1: str, /) -> Value: ...

    def fneg(self, arg0: Value, arg1: str, /) -> Value: ...

    def malloc(self, type: Type, name: str = '') -> CallInst: ...

    def array_malloc(self, type: Type, value: Value, name: str = '') -> CallInst: ...

    def memset(self, ptr: Value, val: Value, len: Value, align: int) -> CallInst: ...

    def memcpy(self, dest: Value, dest_align: int, src: Value, src_align: int, size: Value) -> CallInst:
        """Creates and inserts a memcpy between the specified pointers."""

    def mem_move(self, dest: Value, dest_align: int, src: Value, src_align: int, size: Value) -> CallInst:
        """Creates and inserts a memmove between the specified pointers."""

    def alloca(self, type: Type, name: str = '') -> AllocaInst: ...

    def array_alloca(self, type: Type, value: Value, name: str = '') -> AllocaInst: ...

    def free(self, pointer: Value) -> CallInst: ...

    def load2(self, type: Type, ptr: Value, name: str = '') -> LoadInst: ...

    def store(self, value: Value, ptr: Value) -> StoreInst: ...

    def gep2(self, type: Type, ptr: Value, indices: Sequence[Value], name: str = '') -> Value: ...

    def in_bounds_gep2(self, type: Type, ptr: Value, indices: Sequence[Value], name: str = '') -> Value: ...

    def struct_gep2(self, type: Type, ptr: Value, index: int, name: str = '') -> Value: ...

    def global_string(self, arg0: str, arg1: str, /) -> Value: ...

    def global_string_ptr(self, arg0: str, arg1: str, /) -> Value: ...

    def trunc(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def zext(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def xext(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def fp2ui(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def fp2si(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def ui2fp(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def si2fp(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def fp_trunc(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def fp_ext(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def ptr2int(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def int2ptr(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def bit_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def addr_space_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def zext_or_bit_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def sext_or_bit_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def trunc_or_bit_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def pointer_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def fp_cast(self, val: Value, dest_type: Type, name: str = '') -> Value: ...

    def cast(self, opcode: Opcode, value: Value, dest_type: Type, name: str = '') -> Value: ...

    def int_cast_2(self, value: Value, dest_type: Type, name: str = '') -> Value: ...

    def int_cast(self, value: Value, dest_type: Type, name: str = '') -> Value:
        """Deprecated: This cast is always signed. Use LLVMBuildIntCast2 instead."""

    @staticmethod
    def get_cast_opcode(src: Value, src_is_signed: bool, dest_type: Type, dest_is_signed: bool) -> Opcode: ...

    def icmp(self, op: IntPredicate, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def phi(self, type: Type, name: str = '') -> PHINode: ...

    def call_2(self, fn_type: FunctionType, fn: Function, args: Sequence[Value], name: str = '') -> CallInst: ...

    def call_with_operand_bundles(self, arg0: FunctionType, arg1: Function, arg2: Sequence[Value], arg3: Sequence[OperandBundle], arg4: str, /) -> CallInst: ...

    def select(self, If: Value, Then: Value, Else: Value, name: str = '') -> CallInst: ...

    def vaarg(self, list: Value, type: Type, name: str = '') -> Value: ...

    def extract_element(self, vec: Value, index: Value, name: str = '') -> Value: ...

    def insert_element(self, vec: Value, element: Value, index: Value, name: str = '') -> Value: ...

    def shuffle_vector(self, v1: Value, v2: Value, mask: Value, name: str = '') -> ShuffleVectorInst: ...

    def extract_value(self, agg: Value, index: int, name: str = '') -> Value: ...

    def insert_value(self, agg: Value, elt: Value, index: int, name: str = '') -> Value: ...

    def freeze(self, val: Value, name: str = '') -> Value: ...

    def is_null(self, value: Value, name: str = '') -> Value: ...

    def is_not_null(self, value: Value, name: str = '') -> Value: ...

    def ptr_diff_2(self, elem_type: Type, lhs: Value, rhs: Value, name: str = '') -> Value: ...

    def fence(self, ordering: AtomicOrdering, singleThread: bool, name: str = '') -> FenceInst: ...

    def atomic_rmw(self, op: AtomicRMWBinOp, ptr: Value, val: Value, ordering: AtomicOrdering, singleThread: bool) -> AtomicRMWInst: ...

    def atomic_cmp_xchg(self, arg0: Value, arg1: Value, arg2: Value, arg3: AtomicOrdering, arg4: AtomicOrdering, arg5: bool, /) -> AtomicCmpXchgInst: ...

class CallBase(Instruction):
    """CallBase"""

    @property
    def arg_num(self) -> int: ...

    @property
    def call_conv(self) -> CallConv: ...

    @call_conv.setter
    def call_conv(self, arg: CallConv, /) -> None: ...

    @property
    def called_fn_type(self) -> FunctionType:
        """Obtain the function type called by this instruction."""

    @property
    def called_value(self) -> Function: ...

    @property
    def operand_bundles_num(self) -> int: ...

    def get_operand_bundle_at(self, index: int) -> OperandBundle:
        """
        Obtain the operand bundle attached to this instruction at the given index.
        """

    def set_arg_alignment(self, index: int, align: int) -> None: ...

    def add_call_site_attribute(self, index: int, attr: Attribute) -> None: ...

    def get_call_site_attribute_count(self, arg: int, /) -> int: ...

    def get_call_site_attributes(self, arg: int, /) -> list[Attribute]: ...

    def get_call_site_enum_attribute(self, arg0: int, arg1: int, /) -> EnumAttribute: ...

    def get_call_site_string_attribute(self, arg0: int, arg1: str, /) -> StringAttribute: ...

    def remove_call_site_enum_attribute(self, arg0: int, arg1: int, /) -> None: ...

    def remove_call_site_string_attribute(self, arg0: int, arg1: str, /) -> None: ...

class CallConv(enum.Enum):
    """CallConv"""

    C = 0

    Fast = 8

    Cold = 9

    GHC = 10

    HiPE = 11

    AnyReg = 13

    PreserveMost = 14

    PreserveAll = 15

    Swift = 16

    CXXFASTTLS = 17

    X86Stdcall = 64

    X86Fastcall = 65

    ARMAPCS = 66

    ARMAAPCS = 67

    ARMAAPCSVFP = 68

    MSP430INTR = 69

    X86ThisCall = 70

    PTXKernel = 71

    PTXDevice = 72

    SPIRFUNC = 75

    SPIRKERNEL = 76

    IntelOCLBI = 77

    X8664SysV = 78

    Win64 = 79

    X86VectorCall = 80

    HHVM = 81

    HHVMC = 82

    X86INTR = 83

    AVRINTR = 84

    AVRSIGNAL = 85

    AVRBUILTIN = 86

    AMDGPUVS = 87

    AMDGPUGS = 88

    AMDGPUPS = 89

    AMDGPUCS = 90

    AMDGPUKERNEL = 91

    X86RegCall = 92

    AMDGPUHS = 93

    MSP430BUILTIN = 94

    AMDGPULS = 95

    AMDGPUES = 96

class CallInst(CallBase):
    """CallInst"""

    @property
    def is_tail_call(self) -> bool: ...

    @is_tail_call.setter
    def is_tail_call(self, arg: bool, /) -> None: ...

    @property
    def tail_call_kind(self) -> TailCallKind: ...

    @tail_call_kind.setter
    def tail_call_kind(self, arg: TailCallKind, /) -> None: ...

class CatchPadInst(FuncletPadInst):
    """CatchPadInst"""

    def __repr__(self) -> str: ...

    @property
    def parent(self) -> CatchSwitchInst: ...

    @parent.setter
    def parent(self, arg: CatchSwitchInst, /) -> None: ...

class CatchSwitchInst(Instruction):
    """CatchSwitchInst"""

    def __repr__(self) -> str: ...

    @property
    def unwind_dest(self) -> BasicBlock: ...

    @unwind_dest.setter
    def unwind_dest(self, arg: BasicBlock, /) -> None: ...

    @property
    def handlers_num(self) -> int: ...

    @property
    def handlers(self) -> list[BasicBlock]:
        """
        Obtain the basic blocks acting as handlers for a catchswitch instruction.
        """

    def add_handler(self, arg: BasicBlock, /) -> None: ...

class CleanupReturnInst(Instruction):
    """CleanupReturnInst"""

    def __repr__(self) -> str: ...

    @property
    def unwind_dest(self) -> BasicBlock: ...

    @unwind_dest.setter
    def unwind_dest(self, arg: BasicBlock, /) -> None: ...

class Constant(User):
    """Constant"""

    def __repr__(self) -> str: ...

    @staticmethod
    def null(type: Type) -> Value:
        """Obtain a constant value referring to the null instance of the type."""

    @staticmethod
    def pointer_null(type: Type) -> Value:
        """
        Obtain a constant that is a constant pointer pointing to NULL for thetype.
        """

    @staticmethod
    def all_ones(type: IntType) -> Value:
        """
        Obtain a constant value referring to the instance of the typeconsisting of all ones.
        """

    @staticmethod
    def undef(type: Type) -> UndefValue:
        """Obtain a constant value referring to an undefined value of a type."""

    @staticmethod
    def poison(type: Type) -> PoisonValue:
        """Obtain a constant value referring to a poison value of a type."""

    @property
    def is_null(self) -> bool: ...

class ConstantArray(Constant):
    """ConstantArray"""

    def __init__(self, elem_type: Type, constant_vals: Sequence[Constant]) -> None:
        """Create a ConstantArray from values."""

    def __repr__(self) -> str: ...

    def get_element_at(self, index: int) -> Value | None:
        """
        Returns null if the index is out of range, or it's not possible to determine the element (e.g., because the constant is a constant expression.)
        """

class ConstantDataArray(ConstantDataSequential):
    """ConstantDataArray"""

    def __repr__(self) -> str: ...

    def __str__(self) -> str:
        """Get the given constant data sequential as a string."""

    @staticmethod
    def create_string_in_context(context: Context, str: str, dont_null_terminate: bool) -> ConstantDataArray:
        """Create a ConstantDataSequential and initialize itwith a string."""

    @staticmethod
    def create_string(str: str, dont_null_terminate: bool) -> ConstantDataArray:
        """
        Create a ConstantDataSequential with string contentin the global context.
        """

    @property
    def is_string(self) -> bool:
        """Returns true if the specified constant is an array of i8."""

    def as_string(self) -> str:
        """Get the given constant data sequential as a string."""

class ConstantDataSequential(Constant):
    """ConstantDataSequential"""

class ConstantDataVector(ConstantDataSequential):
    """ConstantDataVector"""

class ConstantExpr(Constant):
    """ConstantExpr"""

    def __repr__(self) -> str: ...

    @property
    def opcode(self) -> Opcode: ...

    def get_icmp_predicate(self) -> IntPredicate:
        """
        Obtain the predicate of an instruction.The opcode needs to be llvm::Instruction::ICmp.
        """

    def get_fcmp_predicate(self) -> RealPredicate:
        """
        Obtain the float predicate of an instruction.The opcode needs to be llvm::Instruction::FCmp.
        """

    @staticmethod
    def get_align_of(type: Type) -> ConstantExpr: ...

    @staticmethod
    def get_size_of(type: Type) -> ConstantExpr: ...

    @staticmethod
    def neg(value: Constant) -> Value: ...

    @staticmethod
    def neg_nsw(value: Constant) -> Value:
        """LLVMConstNSWNeg"""

    @staticmethod
    def neg_nuw(value: Constant) -> Value:
        """LLVMConstNUWNeg"""

    @staticmethod
    def add(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def add_nsw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def add_nuw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def sub(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def sub_nsw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def sub_nuw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def mul(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def mul_nsw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def mul_nuw(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def xor(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def shl(lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def icmp(predicate: IntPredicate, lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def fcmp(predicate: RealPredicate, lhs: Constant, rhs: Constant) -> Value: ...

    @staticmethod
    def gep2(type: Type, value: Constant, indices: Sequence[Value]) -> Value: ...

    @staticmethod
    def gep2_in_bounds(type: Type, value: Constant, indices: Sequence[Value]) -> Value: ...

    @staticmethod
    def trunc(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def ptr2int(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def int2ptr(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def bit_cast(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def addr_space_cast(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def trunc_or_bit_cast(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def pointer_cast(value: Constant, to_type: Type) -> Value: ...

    @staticmethod
    def extract_element(vector: ConstantVector, index: Constant) -> Value: ...

    @staticmethod
    def insert_element(vector: ConstantVector, index: Constant, value: Constant) -> Value: ...

    @staticmethod
    def shuffle_vector(vector_a: ConstantVector, vector_b: ConstantVector, mask: Constant) -> Value: ...

    @staticmethod
    def block_address(arg0: Constant, arg1: BasicBlock, /) -> Value: ...

class ConstantFP(Constant):
    """ConstantFP"""

    @overload
    def __init__(self, real_type: RealType, value: float) -> None:
        """
        Original Function: LLVMConstReal.
        Obtain a constant value referring to a double floating point value.
        """

    @overload
    def __init__(self, type: RealType, text: str) -> None:
        """
        Original Function: LLVMConstRealOfStringAndSize
        Obtain a constant for a floating point value parsed from a string.
        """

    def __repr__(self) -> str: ...

    @property
    def double(self) -> tuple[float, int]:
        """
        Obtain the double value for an floating point constant value.

        The returned value is a tuple, with first one as the doublevalue and the second one indicating whether the some precisionwas lost in the conversion.
        """

class ConstantInt(Constant):
    """ConstantInt"""

    @overload
    def __init__(self, int_type: IntType, value: int, sign_extend: bool) -> None:
        """
        Original Function: LLVMConstInt.
        Obtain a constant value for an integer type.

        Parameters:
        --------int_type: IntTy Integer type to obtain value of.
        value: The value the returned instance should refer to.
        sign_extend: Whether to sign extend the produced value.
        """

    @overload
    def __init__(self, int_type: IntType, num_words: int, words: int) -> None:
        """
        Origin Function: LLVMConstIntOfArbitraryPrecision.
        Obtain a constant value for an integer of arbitrary precision.
        """

    @overload
    def __init__(self, int_type: IntType, text: str, radix: int) -> None:
        """
        Original Function: LLVMConstIntOfStringAndSize
        Obtain a constant value for an integer parsed from a string.
        """

    def __repr__(self) -> str: ...

    @property
    def zext(self) -> int:
        """Obtain the zero extended value."""

    @property
    def sext(self) -> int:
        """Obtain the sign extended value."""

class ConstantStruct(Constant):
    """ConstantStruct"""

    @overload
    def __init__(self, context: Context, constant_values: Sequence[Constant], packed: bool) -> None:
        """Create an anonymous ConstantStruct with the specifiedvalues."""

    @overload
    def __init__(self, struct_type: Type, constant_values: Sequence[Constant]) -> None:
        """Create a non-anonymous ConstantStruct from values."""

    def __repr__(self) -> str: ...

    def get_element_at(self, index: int) -> Value | None:
        """
        Returns null if the index is out of range, or it's not possible to determine the element (e.g., because the constant is a constant expression.)
        """

class ConstantVector(Constant):
    """ConstantVector"""

    def __init__(self, values: Sequence[Constant]) -> None: ...

    def __repr__(self) -> str: ...

    def get_element_at(self, index: int) -> Value | None:
        """
        Returns null if the index is out of range, or it's not possible to determine the element (e.g., because the constant is a constant expression.)
        """

class Context(llvmpym_ext.PymContextObject):
    """
    Contexts are execution states for the core LLVM IR system.

    Most types are tied to a context instance. Multiple contexts canexist simultaneously. A single context is not thread safe. However,different contexts can execute on different threads simultaneously.
    """

    def __init__(self) -> None:
        """Create a new context."""

    def __repr__(self) -> str: ...

    def __enter__(self) -> Context: ...

    def __exit__(self, *args, **kwargs) -> None: ...

    @staticmethod
    def get_global_context() -> Context:
        """Obtain the global context instance."""

    @property
    def diagnostic_context(self) -> types.CapsuleType:
        """Get the diagnostic context of this context."""

    @property
    def should_discard_value_names(self) -> bool:
        """
        Retrieve whether the given context is set todiscard all value names.

        Return true if the Context runtime configuration is set to discard all value names. When true, only GlobalValue names will be available in the IR.
        """

    @should_discard_value_names.setter
    def should_discard_value_names(self, arg: bool, /) -> None:
        """
        Set whether the given context discards all value names.

        If true, only the names of GlobalValue objectswill be available in the IR.
        This can be used to save memory and runtime, especially in release mode.
        """

    def set_diagnostic_handler(self, handler: Callable[[DiagnosticInfo, object], None], diagnostic_context: Any) -> None:
        """Set the diagnostic handler for this context."""

    def get_diagnostic_handler(self) -> Callable[[DiagnosticInfo, object], None]:
        """Get the diagnostic handler of this context."""

    def parse_ir(self, memory_buffer: MemoryBuffer) -> Module:
        """
        Read LLVM IR from a memory buffer and convert it into an in-memory Moduleobject.

        :raises RuntimeError
        NOTE that you cannot use passed-in memory_buffer after this operation.
        """

    def create_builder(self) -> Builder: ...

    def parse_bitcode(self, mem_buf: MemoryBuffer) -> Module:
        """
        Builds a module from the bitcode in the specified memory buffer, returning a reference to the module
        """

    def get_bitcode_module(self, mem_buf: MemoryBuffer) -> Module:
        """
        Reads a module from the given memory buffer.
        Takes ownership of MemBuf if (and only if) the module was read successfully
        """

    def create_basic_block(self, name: str = '') -> BasicBlock:
        """Create a new basic block without inserting it into a function."""

    def append_basic_block(self, fn: Function, name: str = '') -> BasicBlock:
        """Append a basic block to the end of a function."""

    def insert_basic_block(self, bb: BasicBlock, name: str = '') -> BasicBlock:
        """
        Insert a basic block in a function before another basic block.

        The function to add to is determined by the function of thepassed basic block.
        """

    def get_md_kind_id(self, name: str = '') -> int: ...

    def create_enum_attribute(self, kind_id: int, val: int) -> EnumAttribute:
        """Create an enum attribute."""

    def create_type_attribute(self, kind_id: int, type: Type) -> TypeAttribute:
        """Create a type attribute"""

    def create_string_attribute(self, arg0: str, arg1: str, /) -> StringAttribute: ...

    def get_type_by_name_2(self, name: str = '') -> Type | None: ...

    def create_md_string_2(self, name: str = '') -> MDString:
        """Create an MDString value from a given string value."""

    def create_md_node_2(self, metadata: Sequence[Metadata]) -> MDNode: ...

    def get_metadata_as_value(self, arg: Metadata, /) -> MetadataAsValue: ...

class DLLStorageClass(enum.Enum):
    """DLLStorageClass"""

    Default = 0

    DLLImport = 1
    """Function to be imported from DLL."""

    DLLExport = 2
    """Function to be accessible from DLL."""

class DiagnosticInfo(llvmpym_ext.PymDiagnosticInfoObject):
    """DiagnosticInfo"""

    def __repr__(self) -> str: ...

    def __str__(self) -> str:
        """Return a string representation of the DiagnosticInfo."""

    @property
    def severity(self) -> DiagnosticSeverity:
        """Return an enum LLVMDiagnosticSeverity."""

class DiagnosticSeverity(enum.Enum):
    """DiagnosticSeverity"""

    Error = 0

    Warning = 1

    Remark = 2

    Note = 3

class EnumAttribute(Attribute):
    """EnumAttribute"""

    def __init__(self, context: Context, kind_id: int, val: int) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def kind(self) -> int: ...

    @property
    def value(self) -> int:
        """Get the enum attribute's value. 0 is returned if none exists."""

    @staticmethod
    def get_enum_attribute_kind_for_name(name: str = '') -> int:
        """
        Return an unique id given the name of a enum attribute,or 0 if no attribute by that name exists.

        See http://llvm.org/docs/LangRef.html#parameter-attributesand http://llvm.org/docs/LangRef.html#function-attributesfor the list of available attributes.

        NB: Attribute names and/or id are subject to change withoutgoing through the C API deprecation cycle.
        """

    @staticmethod
    def get_last_enum_attribute_kind() -> int: ...

class ExtractValueInst(IEValueInstBase):
    """ExtractValueInst"""

class FCmpInst(Instruction):
    """FCmpInst"""

    def __repr__(self) -> str: ...

    @property
    def predicate(self) -> RealPredicate:
        """Obtain the float predicate of an instruction."""

class FenceInst(Instruction):
    """FenceInst"""

    def __repr__(self) -> str: ...

    @property
    def ordering(self) -> AtomicOrdering: ...

    @ordering.setter
    def ordering(self, arg: AtomicOrdering, /) -> None: ...

    @property
    def is_single_thread(self) -> bool: ...

    @is_single_thread.setter
    def is_single_thread(self, arg: bool, /) -> None: ...

class FuncletPadInst(Instruction):
    """FuncletPadInst"""

    def __repr__(self) -> str: ...

    @property
    def arg_num(self) -> int: ...

    def get_arg_operand(self, index: int) -> Value: ...

    def set_arg_operand(self, arg0: int, arg1: Value, /) -> None: ...

class Function(GlobalObject):
    """Function"""

    def __init__(self, module: Module, function_type: FunctionType, name: str = '') -> None:
        """Add a function to a module under a specified name."""

    def __repr__(self) -> str: ...

    @property
    def call_conv(self) -> CallConv: ...

    @call_conv.setter
    def call_conv(self, arg: CallConv, /) -> None: ...

    @property
    def gc(self) -> str:
        """
        Obtain the name of the garbage collector to use during code generation.
        """

    @gc.setter
    def gc(self, arg: str, /) -> None: ...

    @property
    def basic_blocks_num(self) -> int: ...

    @property
    def basic_blocks(self) -> list[BasicBlock]: ...

    @property
    def first_basic_block(self) -> BasicBlock | None: ...

    @property
    def last_basic_block(self) -> BasicBlock | None: ...

    @property
    def entry_basic_block(self) -> BasicBlock: ...

    @property
    def has_personality_fn(self) -> bool: ...

    @property
    def personality_fn(self) -> Function: ...

    @personality_fn.setter
    def personality_fn(self, arg: Function, /) -> None: ...

    @property
    def intrinsic_id(self) -> int: ...

    @property
    def next(self) -> Function | None:
        """
        Advance a Function iterator to the next Function.

        Returns NULL if the iterator was already at the end and there are no morefunctions.
        """

    @property
    def previous(self) -> Function | None:
        """
        Decrement a Function iterator to the previous Function.

        Returns NULL if the iterator was already at the beginning and there areno previous functions.
        """

    @property
    def debug_loc_directory(self) -> str:
        """Return the directory of the debug location for this value"""

    @property
    def debug_loc_filename(self) -> str:
        """Return the filename of the debug location for this value"""

    @property
    def debug_loc_line(self) -> int:
        """Return the line number of the debug location for this value"""

    @property
    def arg_num(self) -> int: ...

    @property
    def first_arg(self) -> Argument | None: ...

    @property
    def last_arg(self) -> Argument | None: ...

    @property
    def args(self) -> list[Argument]: ...

    def verify(self, action: llvmpym_ext.analysis.VerifierFailureAction) -> str | None:
        """
        Verifies that a single function is valid, taking the specified action. Usefufor debugging.
        """

    def get_arg(self, index: int) -> Argument:
        """
        Obtain the parameter at the specified index.

        Parameters are indexed from 0.
        """

    def destory(self) -> None:
        """
        Remove a function from its containing module and deletes it.

        Note you shouldn't use the the variable afterwards!
        """

    def add_attribute_at_index(self, index: int, attr: Attribute) -> None: ...

    def append_existing_basic_block(self, basic_block: BasicBlock) -> None:
        """
        Append the given basic block to the basic block list of the given function.
        """

    def append_basic_block(self, name: str = '') -> BasicBlock:
        """
        Append a basic block to the end of a function using the global context.
        """

    def get_attribute_count_at_index(self, index: int) -> int: ...

    def get_attributes_at_index(self, index: int) -> list[Attribute]: ...

    def get_enum_attribute_at_index(self, index: int, kind: int) -> EnumAttribute: ...

    def get_string_attribute_at_index(self, index: int, kind: str) -> StringAttribute: ...

    def remove_enum_attribute_at_index(self, index: int, kind: int) -> None: ...

    def remove_string_attribute_at_index(self, index: int, kind: str) -> None: ...

    def add_target_dependent_attr(self, A: str, V: str) -> None:
        """Add a target-dependent attribute to a function"""

FunctionAttributeIndex: int = 4294967295

class FunctionIterator:
    """FunctionIterator"""

    def __iter__(self) -> FunctionIterator: ...

    def __next__(self) -> Function: ...

class FunctionPassManager(PassManager):
    """FunctionPassManager"""

    def __init__(self, module: Module) -> None:
        """
        Constructs a new function-by-function pass pipeline over the moduleprovider. It does not take ownership of the module provider. This type ofpipeline is suitable for code generation and JIT compilation tasks.
        """

    def __repr__(self) -> str: ...

    def initialize(self) -> bool:
        """
        Initializes all of the function passes scheduled in the function passmanager. Returns true if any of the passes modified the module, false otherwise.
        """

    def run(self, f: Function) -> bool:
        """
        Executes all of the function passes scheduled in the function pass manageron the provided function. Returns true if any of the passes modified thefunction, false otherwise.
        """

    def finalize(self) -> bool:
        """
        Finalizes all of the function passes scheduled in the function passmanager. Returns 1 if any of the passes modified the module, 0 otherwise.
        """

class FunctionType(Type):
    """FunctionType"""

    def __init__(self, return_type: Type, param_types: Sequence[Type], is_var_arg: bool) -> None:
        """Obtain a function type consisting of a specified signature."""

    def __repr__(self) -> str: ...

    @property
    def is_vararg(self) -> bool:
        """Returns whether a function type is variadic."""

    @property
    def return_type(self) -> Type:
        """Obtain the Type this function Type returns."""

    @property
    def params_num(self) -> int:
        """Obtain the number of parameters this function accepts."""

    @property
    def param_types(self) -> list[FunctionType]:
        """Obtain the types of a function's parameters."""

class GetElementPtrInst(Instruction):
    """GetElementPtrInst"""

    def __repr__(self) -> str: ...

    @property
    def indices_num(self) -> int: ...

    @property
    def is_bounds(self) -> bool: ...

    @is_bounds.setter
    def is_bounds(self, arg: bool, /) -> None: ...

    @property
    def source_element_type(self) -> Type: ...

class GlobalAlias(GlobalValue):
    """GlobalAlias"""

    def __init__(self, module: Module, value_type: Type, addr_space: int, aliasee: Value, name: str = '') -> None:
        """
        Add a GlobalAlias with the given value type, address space and aliasee.
        """

    def __repr__(self) -> str: ...

    @property
    def next(self) -> GlobalAlias | None:
        """
        Advance a GlobalAlias iterator to the next GlobalAlias.

        Returns NULL if the iterator was already at the beginning and there areno previous global aliases.
        """

    @property
    def prev(self) -> GlobalAlias | None:
        """
        Decrement a GlobalAlias iterator to the previous GlobalAlias.

        Returns NULL if the iterator was already at the beginning and there areno previous global aliases.
        """

    @property
    def aliasee(self) -> Value: ...

    @aliasee.setter
    def aliasee(self, arg: Value, /) -> None: ...

class GlobalAliasIterator:
    """GlobalAliasIterator"""

    def __iter__(self) -> GlobalAliasIterator: ...

    def __next__(self) -> GlobalAlias: ...

class GlobalIFunc(GlobalObject):
    """GlobalIFunc"""

    def __repr__(self) -> str: ...

    @property
    def next(self) -> GlobalIFunc | None: ...

    @property
    def prev(self) -> GlobalIFunc | None: ...

    @property
    def resolver(self) -> Constant | None: ...

    @resolver.setter
    def resolver(self, arg: Constant, /) -> None: ...

    def destory(self) -> None:
        """
        Remove a global indirect function from its parent module and delete it.

        You shouldn't use it anymore after removal.
        """

    def remove_from_parent(self) -> None:
        """
        Remove a global indirect function from its parent module.

        This unlinks the global indirect function from its containing module butkeeps it alive.
        """

class GlobalIFuncIterator:
    """GlobalIFuncIterator"""

    def __iter__(self) -> GlobalIFuncIterator: ...

    def __next__(self) -> GlobalIFunc: ...

class GlobalObject(GlobalValue):
    """GlobalObject"""

    def __repr__(self) -> str: ...

    def set_metadata(self, arg0: int, arg1: Metadata, /) -> None:
        """
        Sets a metadata attachment, erasing the existing metadata attachment ifit already exists for the given kind.
        """

    def erase_metadata(self, arg: int, /) -> None:
        """Erases a metadata attachment of the given kind if it exists."""

    def clear_metadata(self) -> None:
        """Removes all metadata attachments from this value."""

    def copy_all_metadata(self) -> MetadataEntry:
        """
        Retrieves an array of metadata entries representing the metadata attached tothis value.
        """

class GlobalValue(Constant):
    """GlobalValue"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def parent(self) -> Module: ...

    @property
    def is_declaration(self) -> bool: ...

    @property
    def linkage(self) -> Linkage: ...

    @linkage.setter
    def linkage(self, linkage: Linkage, /) -> None: ...

    @property
    def section(self) -> str | None: ...

    @section.setter
    def section(self, section: str, /) -> None: ...

    @property
    def visibility(self) -> Visibility: ...

    @visibility.setter
    def visibility(self, visibility: Visibility, /) -> None: ...

    @property
    def dll_storage_class(self) -> DLLStorageClass: ...

    @dll_storage_class.setter
    def dll_storage_class(self, arg: DLLStorageClass, /) -> None: ...

    @property
    def unnamed_address(self) -> UnnamedAddr: ...

    @unnamed_address.setter
    def unnamed_address(self, addr: UnnamedAddr) -> None: ...

    @property
    def value_type(self) -> Type:
        """
        Returns the "value type" of a global value.  This differs from the formal type of a global value which is always a pointer type.
        """

class GlobalVariable(GlobalObject):
    """GlobalVariable"""

    def __init__(self, module: Module, type: Type, name: str = '') -> None: ...

    def __repr__(self) -> str: ...

    @property
    def initializer(self) -> Value: ...

    @initializer.setter
    def initializer(self, value: Constant) -> None: ...

    @property
    def is_thread_local(self) -> bool: ...

    @is_thread_local.setter
    def is_thread_local(self, arg: bool, /) -> None: ...

    @property
    def is_global_constant(self) -> bool: ...

    @is_global_constant.setter
    def is_global_constant(self, is_constant: bool, /) -> None: ...

    @property
    def thread_local_mode(self) -> ThreadLocalMode: ...

    @thread_local_mode.setter
    def thread_local_mode(self, mode: ThreadLocalMode, /) -> None: ...

    @property
    def is_externally_initialized(self) -> bool: ...

    @is_externally_initialized.setter
    def is_externally_initialized(self, is_ext_init: bool, /) -> None: ...

    @property
    def next(self) -> GlobalVariable | None: ...

    @property
    def prev(self) -> GlobalVariable | None: ...

    @property
    def debug_loc_directory(self) -> str:
        """Return the directory of the debug location for this value"""

    @property
    def debug_loc_filename(self) -> str:
        """Return the filename of the debug location for this value"""

    @property
    def debug_loc_line(self) -> int:
        """Return the line number of the debug location for this value"""

    def destory(self) -> None:
        """Delete this variable. You are not supposed to use this variable later."""

class GlobalVariableIterator:
    """GlobalVariableIterator"""

    def __iter__(self) -> GlobalVariableIterator: ...

    def __next__(self) -> GlobalVariable: ...

class ICmpInst(Instruction):
    """ICmpInst"""

    def __repr__(self) -> str: ...

    @property
    def predicate(self) -> IntPredicate:
        """Obtain the predicate of an instruction."""

class IEValueInstBase(Instruction):
    """IEValueInstBase"""

    @property
    def indices_num(self) -> int: ...

    def indices(self) -> int: ...

class IndirectBrInst(Instruction):
    """IndirectBrInst"""

    def __repr__(self) -> str: ...

    def add_destination(self, dest: BasicBlock) -> None:
        """Add a destination to the indirectbr instruction."""

class InlineAsm(Value):
    """InlineAsm"""

    def __repr__(self) -> str: ...

    def get_inline_asm(self, type: Type, asm: str, constraints: str, has_side_effects: bool, is_align_stack: bool, dialect: InlineAsmDialect, can_throw: bool) -> None:
        """Create the specified unique inline asm string."""

    @property
    def str(self) -> str:
        """Get the template string used for an inline assembly snippet."""

    @property
    def constraint_str(self) -> str:
        """Get the raw constraint string for an inline assembly snippet."""

    @property
    def dialect(self) -> InlineAsmDialect:
        """Get the dialect used by the inline asm snippet."""

    @property
    def function_type(self) -> FunctionType:
        """
        Get the function type of the inline assembly snippet. The same type that was passed into :func:`get_inline_asm` originally.
        """

    @property
    def has_side_effects(self) -> bool:
        """Get if the inline asm snippet has side effects."""

    @property
    def needs_aligned_stack(self) -> bool: ...

    @property
    def can_unwind(self) -> bool: ...

class InlineAsmDialect(enum.Enum):
    """InlineAsmDialect"""

    ATT = 0

    Intel = 1

class InsertValueInst(IEValueInstBase):
    """InsertValueInst"""

class Instruction(User):
    """Instruction"""

    def __repr__(self) -> str: ...

    @property
    def can_use_fast_math_flags(self) -> bool:
        """
        Check if a given value can potentially have fast math flags.
        Will return true for floating point arithmetic instructions, and for select, phi, and call instructions whose type is a floating point type, or a vector or array thereof.
        See https://llvm.org/docs/LangRef.html#fast-math-flags
        """

    @property
    def next(self) -> Instruction | None:
        """
        Obtain the instruction that occurs after the one specified.
        The next instruction will be from the same basic block.

        If this is the last instruction in a basic block, None will be returned.
        """

    @property
    def prev(self) -> Instruction | None:
        """
        Obtain the instruction that occurred before this one.

        If the instruction is the first instruction in a basic block, NULLwill be returned.
        """

    @property
    def has_metadata(self) -> bool: ...

    @property
    def debug_loc_directory(self) -> str:
        """Return the directory of the debug location for this value"""

    @property
    def debug_loc_filename(self) -> str:
        """Return the filename of the debug location for this value."""

    @property
    def debug_loc_line(self) -> int:
        """Return the line number of the debug location for this value"""

    @property
    def debug_loc_column(self) -> int:
        """Return the column number of the debug location for this value"""

    @property
    def parent(self) -> BasicBlock | None:
        """Obtain the basic block to which an instruction belongs."""

    @property
    def opcode(self) -> Opcode: ...

    @property
    def is_terminator(self) -> bool: ...

    def clone(self) -> Instruction | None:
        """
        Create a copy of 'this' instruction that is identical in all waysexcept the following:
          - The instruction has no parent  - The instruction has no name
        """

    def remove_from_parent(self) -> None:
        """
        The instruction specified is removed from its containing buildingblock but is kept alive.
        """

    def destory(self) -> None:
        """
        Remove and delete an instruction.

        The instruction specified is removed from its containing buildingblock and then deleted.
        """

    def delete(self) -> None:
        """
        Delete an instruction.

        The instruction specified is deleted. It must have previously beenremoved from its containing building block.
        """

    def get_metadata(self, kind_id: int) -> Value | None: ...

    def set_metadata(self, kind_id: int, value: MetadataAsValue) -> None: ...

    def get_all_metadata_no_debug_loc(self) -> MetadataEntry: ...

    @property
    def successors_num(self) -> int: ...

    def get_successor(self, arg: int, /) -> BasicBlock: ...

    def set_successor(self, arg0: int, arg1: BasicBlock, /) -> None: ...

    @staticmethod
    def get_nuw(arith_inst: Instruction) -> bool: ...

    @staticmethod
    def set_nuw(arith_inst: Instruction, hasNUW: bool) -> None: ...

    @staticmethod
    def get_nsw(arithInst: Instruction) -> bool: ...

    @staticmethod
    def set_nsw(arith_inst: Instruction, hasNSW: bool) -> None: ...

    @staticmethod
    def get_exact(div_or_shr_inst: Instruction) -> bool: ...

    @staticmethod
    def set_exact(div_or_shr_inst: Instruction, is_exact: bool) -> None: ...

    @staticmethod
    def get_nneg(non_neg_inst: Instruction) -> bool:
        """Only valid for zext instructions."""

    @staticmethod
    def set_nned(non_neg_inst: Instruction, is_non_neg: bool) -> None:
        """
        Sets the non-negative flag for the instruction.
        Only valid for zext instructions.
        """

    @staticmethod
    def get_fast_math_flags(fp_math_inst: Instruction) -> int:
        """
        Get the flags for which fast-math-style optimizations are allowed for this value.

        Only valid on floating point instructions.See `can_use_fast_math_flags`.
        """

    @staticmethod
    def set_fast_math_flags(fp_math_inst: Instruction, fmf: int) -> None:
        """
        Sets the flags for which fast-math-style optimizations are allowed for this value.

        Only valid on floating point instructions.
        See `can_use_fast_math_flags`.
        """

    @staticmethod
    def get_is_disjoint(inst: Instruction) -> bool:
        """
        Gets whether the instruction has the disjoint flag set.
        Only valid for or instructions.
        """

    @staticmethod
    def set_is_disjoint(inst: Instruction, is_disjoint: bool) -> None:
        """
        Sets the disjoint flag for the instruction.
        Only valid for or instructions.
        """

class InstructionIterator:
    """InstructionIterator"""

    def __iter__(self) -> InstructionIterator: ...

    def __next__(self) -> Instruction: ...

class IntPredicate(enum.Enum):
    """IntPredicate"""

    EQ = 32
    """equal"""

    NE = 33
    """not equal"""

    UGT = 34
    """unsigned greater than"""

    UGE = 35
    """unsigned greater or equal"""

    ULT = 36
    """unsigned less than"""

    ULE = 37
    """unsigned less or equal"""

    SGT = 38
    """signed greater than"""

    SGE = 39
    """signed greater or equal"""

    SLT = 40
    """signed less than"""

    SLE = 41
    """signed less or equal"""

class IntType(Type):
    """IntType"""

    def __init__(self, context: Context, num_bits: int) -> None: ...

    def __repr__(self) -> str: ...

    @staticmethod
    def Int1(context: Context) -> IntType: ...

    @staticmethod
    def Int8(context: Context) -> IntType: ...

    @staticmethod
    def Int16(context: Context) -> IntType: ...

    @staticmethod
    def Int32(context: Context) -> IntType: ...

    @staticmethod
    def Int64(context: Context) -> IntType: ...

    @staticmethod
    def Int128(context: Context) -> IntType: ...

    GlobalInt1: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    GlobalInt8: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    GlobalInt16: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    GlobalInt32: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    GlobalInt64: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    GlobalInt128: llvmpym_ext.core.IntType = ...
    """Get type from global context."""

    @staticmethod
    def Global(arg: int, /) -> IntType:
        """Get type from global context."""

    @property
    def width(self) -> int: ...

    def all_ones(self) -> Value:
        """
        Obtain a constant value referring to the instance of the typeconsisting of all ones.
        """

class Intrinsic(llvmpym_ext.PymIntrinsicObject):
    """Intrinsic"""

    @overload
    def __repr__(self) -> str: ...

    @overload
    def __repr__(self) -> str: ...

    def __bool__(self) -> bool: ...

    @staticmethod
    def lookup(name: str = '') -> Intrinsic:
        """Obtain the intrinsic ID number which matches the given function name."""

    def get_type(self, context: Context, param_types: Sequence[Type]) -> FunctionType:
        """
        Retrieves the type of an intrinsic.  For overloaded intrinsics, parameter types must be provided to uniquely identify an overload.
        """

    @property
    def id(self) -> int: ...

    @property
    def name(self) -> str:
        """Retrieves the name of an intrinsic."""

    @property
    def is_overloaded(self) -> bool: ...

    def copy_overloaded_name(self, param_types: Sequence[Type]) -> str:
        """Deprecated: Use :func:`copy_overloaded_name2` instead."""

    def copy_overloaded_name2(self, module: Module, param_types: Sequence[Type]) -> str:
        """
        Copies the name of an overloaded intrinsic identified by a given list of parameter types.

        This version also supports unnamed types.
        """

class InvokeInst(CallBase):
    """InvokeInst"""

    def __repr__(self) -> str: ...

    @property
    def normal_dest(self) -> BasicBlock: ...

    @normal_dest.setter
    def normal_dest(self, arg: BasicBlock, /) -> None: ...

    @property
    def unwind_dest(self) -> BasicBlock: ...

    @unwind_dest.setter
    def unwind_dest(self, arg: BasicBlock, /) -> None: ...

class LabelType(Type):
    """LabelType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

    Global: llvmpym_ext.core.LabelType = ...
    """(arg: object, /) -> llvmpym_ext.core.LabelType"""

class LandingPadClauseTy(enum.Enum):
    """LandingPadClauseTy"""

    Catch = 0
    """A catch clause"""

    Filter = 1
    """A filter clause"""

class LandingPadInst(Instruction):
    """LandingPadInst"""

    def __repr__(self) -> str: ...

    @property
    def num_clauses(self) -> int: ...

    @property
    def is_cleanup(self) -> bool: ...

    @is_cleanup.setter
    def is_cleanup(self, arg: bool, /) -> None: ...

    def get_clause(self, index: int) -> Value: ...

    def add_clause(self, arg: Constant, /) -> None: ...

class Linkage(enum.Enum):
    """Linkage"""

    External = 0
    """Externally visible function"""

    AvailableExternally = 1

    LinkOnceAny = 2
    """Keep one copy of function when linking (inline)"""

    LinkOnceODR = 3
    """
    Keep one copy of function when linking (inline), but only replaced by something equivalent.
    """

    LinkOnceODRAutoHide = 4
    """Obsolete"""

    WeakAny = 5
    """Keep one copy of function when linking (weak)"""

    WeakODR = 6
    """Same, but only replaced by something equivalent."""

    Appending = 7
    """Special purpose, only applies to global arrays"""

    Internal = 8
    """Rename collisions when linking (static functions)"""

    Private = 9
    """Like Internal, but omit from symbol table"""

    DLLImport = 10
    """Obsolete"""

    DLLExport = 11
    """Obsolete"""

    ExternalWeak = 12
    """ExternalWeak linkage description"""

    Ghost = 13
    """Obsolete"""

    Common = 14
    """Tentative definitions"""

    LinkerPrivate = 15
    """Like Private, but linker removes."""

    LinkerPrivateWeak = 16
    """Like LinkerPrivate, but is weak."""

class LoadInst(Instruction):
    """LoadInst"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def is_volatile(self) -> bool: ...

    @is_volatile.setter
    def is_volatile(self, arg: bool, /) -> None: ...

    @property
    def ordering(self) -> AtomicOrdering: ...

    @ordering.setter
    def ordering(self, arg: AtomicOrdering, /) -> None: ...

    @property
    def is_single_thread(self) -> bool: ...

    @is_single_thread.setter
    def is_single_thread(self, arg: bool, /) -> None: ...

class MDNode(Metadata):
    """MDNode"""

    def __init__(self, context: Context, metadata: Sequence[Metadata]) -> None: ...

    def __repr__(self) -> str: ...

    def as_value(self, context: Context) -> MDNodeValue: ...

class MDNodeValue(MetadataAsValue):
    """MDNodeValue"""

    def __repr__(self) -> str: ...

    def as_metadata(self) -> MDNode: ...

    @property
    def num_operands(self) -> int: ...

    @property
    def operands(self) -> list[Value]:
        """Obtain the given MDNode's operands."""

    @property
    def replace_operand_with(self, arg0: int, arg1: Metadata, /) -> None:
        """Replace an operand at a specific index in a llvm::MDNode value."""

class MDString(Metadata):
    """MDString"""

    def __init__(self, context: Context, name: str = '') -> None:
        """Create an MDString value from a given string value."""

    def __repr__(self) -> str: ...

    def as_value(self, context: Context) -> MDStringValue: ...

class MDStringValue(MetadataAsValue):
    """MDStringValue"""

    def __repr__(self) -> str: ...

    def as_metadata(self) -> MDString: ...

    @property
    def raw_string(self) -> str:
        """Obtain the underlying string from a MDString value."""

class MemoryBuffer(llvmpym_ext.PymMemoryBufferObject):
    """MemoryBuffer"""

    def __repr__(self) -> str: ...

    @staticmethod
    def from_file(path: str) -> MemoryBuffer:
        """:raises RuntimeError"""

    @staticmethod
    def from_stdin() -> MemoryBuffer:
        """:raises RuntimeError"""

    @overload
    @staticmethod
    def from_str(input_data: str, requires_null_terminator: bool, buffer_name: str = '') -> MemoryBuffer: ...

    @overload
    @staticmethod
    def from_str(input_data: str, buffer_name: str = '') -> MemoryBuffer | None: ...

    @property
    def buffer_start(self) -> str: ...

    @property
    def buffer_size(self) -> int: ...

class Metadata(llvmpym_ext.PymMetadataObject):
    """Metadata"""

    def __repr__(self) -> str: ...

    @staticmethod
    def get_md_kind_id(name: str = '') -> int: ...

    def as_value(self, context: Context) -> MetadataAsValue: ...

class MetadataAsValue(Value):
    """MetadataAsValue"""

class MetadataEntry(llvmpym_ext.PymMetadataEntriesObject):
    """MetadataEntry"""

    def __repr__(self) -> str: ...

    def get_kind(self, index: int) -> int:
        """Returns the kind of a value metadata entry at a specific index."""

    def get_metadata(self, index: int) -> Metadata:
        """
        Returns the underlying metadata node of a value metadata entry at aspecific index.
        """

class MetadataType(Type):
    """MetadataType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

class Module(llvmpym_ext.PymModuleObject):
    """
    Modules represent the top-level structure in an LLVM program. An LLVMmodule is effectively a translation unit or a collection of translation units merged together.
    """

    def __init__(self, name: str = '') -> None: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str:
        """Return a string representation of the module"""

    def __enter__(self) -> Module: ...

    def __exit__(self, *args, **kwargs) -> None: ...

    @property
    def data_layout(self) -> str:
        """Obtain the data layout for a module."""

    @data_layout.setter
    def data_layout(self, arg: str, /) -> None:
        """Set the data layout for a module."""

    @property
    def first_global_variable(self) -> GlobalVariable | None: ...

    @property
    def last_global_variable(self) -> GlobalVariable | None: ...

    @property
    def global_variables(self) -> GlobalVariableIterator: ...

    @property
    def first_global_ifunc(self) -> GlobalIFunc | None: ...

    @property
    def last_global_ifunc(self) -> GlobalIFunc | None: ...

    @property
    def global_ifuncs(self) -> GlobalIFuncIterator: ...

    @property
    def first_global_alias(self) -> GlobalAlias | None: ...

    @property
    def last_global_alias(self) -> GlobalAlias | None: ...

    @property
    def global_aliases(self) -> GlobalAliasIterator: ...

    @property
    def first_named_metadata(self) -> NamedMDNode | None:
        """Obtain an iterator to the first NamedMDNode in a Module."""

    @property
    def last_named_metadata(self) -> NamedMDNode | None:
        """Obtain an iterator to the last NamedMDNode in a Module."""

    @property
    def named_metadatas(self) -> NamedMDNodeIterator:
        """Obtain an iterator to the first NamedMDNode in a Module."""

    @property
    def context(self) -> Context:
        """Obtain the context to which this module is associated."""

    @property
    def id(self) -> str:
        """
        Get the module identifier.
        Origin Function: LLVMSetModuleIdentifier.
        """

    @id.setter
    def id(self, arg: str, /) -> None:
        """
        Set the module identifier.
        Origin Function: LLVMGetModuleIdentifier.
        """

    @property
    def source_file_name(self) -> str: ...

    @source_file_name.setter
    def source_file_name(self, name: str = '') -> None: ...

    @property
    def target(self) -> str:
        """Obtain the target triple for a module."""

    @target.setter
    def target(self, arg: str, /) -> None:
        """Set the target triple for a module."""

    @property
    def inline_asm(self) -> str: ...

    @inline_asm.setter
    def inline_asm(self, arg: str, /) -> None: ...

    @property
    def first_function(self) -> Function:
        """Obtain an iterator to the first Function in a Module."""

    @property
    def last_function(self) -> Function:
        """Obtain an iterator to the last Function in a Module."""

    @property
    def functions(self) -> FunctionIterator: ...

    def create_function_pass_manager(self) -> FunctionPassManager:
        """
        Constructs a new function-by-function pass pipeline over the moduleprovider. It does not take ownership of the module provider. This type ofpipeline is suitable for code generation and JIT compilation tasks.
        """

    def create_module_provider(self) -> ModuleProvider: ...

    def write_bitcode_to_file(self, path: str) -> int: ...

    def write_bitcode_to_memory_buffer(self) -> MemoryBuffer: ...

    def get_intrinsic_declaration(self, id: int, param_types: Sequence[Type]) -> Function:
        """
        Create or insert the declaration of an intrinsic.  For overloaded intrinsics,parameter types must be provided to uniquely identify an overload.
        """

    def verify(self, action: llvmpym_ext.analysis.VerifierFailureAction) -> str | None:
        """
        Verifies that a module is valid, taking the specified action if not.
        Returns:
        	If success, return None. Otherwise, optionally(based on action) return a human-readable description if any invalid constructs.
        """

    def add_alias(self, value_type: Type, addr_space: int, aliasee: Value, name: str = '') -> GlobalAlias:
        """
        Add a GlobalAlias with the given value type, address space and aliasee.
        """

    def get_named_global_alias(self, name: str = '') -> GlobalAlias:
        """Obtain a GlobalAlias value from by its name."""

    def add_global(self, type: Type, name: str = '') -> GlobalVariable: ...

    def add_global_in_address_space(self, type: Type, name: str = '', address_space: int = 0) -> GlobalVariable: ...

    def get_named_global(self, arg: str, /) -> GlobalVariable: ...

    def add_global_indirect_func(self, type: Type, addr_space: int, resolver: Constant, name: str = '') -> GlobalIFunc: ...

    def get_named_global_ifunc(self, arg: str, /) -> GlobalIFunc | None: ...

    def add_function(self, function_type: FunctionType, name: str = '') -> Function:
        """Add a function to a module under a specified name."""

    def get_named_function(self, name: str = '') -> Function:
        """Obtain a Function value from a Module by its name."""

    def get_named_metadata(self, name: str = '') -> NamedMDNode | None:
        """
        Retrieve a NamedMDNode with the given name, returning NULL if no suchnode exists.
        """

    def get_or_insert_named_metadata(self, name: str = '') -> NamedMDNode:
        """
        Retrieve a NamedMDNode with the given name, creating a new node if no suchnode exists.
        """

    def get_named_metadata_operands_num(self, name: str = '') -> int:
        """Obtain the number of operands for named metadata in a module."""

    def get_named_metadata_operands(self, name: str = '') -> list[Value]:
        """
        Obtain the named metadata operands for a module.

        The passed LLVMValueRef pointer should refer to an array ofLLVMValueRef at least LLVMGetNamedMetadataNumOperands long. Thisarray will be populated with the LLVMValueRef instances. Eachinstance corresponds to a llvm::MDNode.
        """

    def add_named_metadata_operand(self, arg0: str, arg1: Value, /) -> None:
        """Add an operand to named metadata."""

    def clone(self) -> Module:
        """Return an exact copy of the specified module."""

    def copy_module_flags_metadata(self) -> ModuleFlagEntry:
        """Returns the module flags as an array of flag-key-value triples."""

    def get_flag(self, key: str) -> Metadata | None:
        """
        Return the corresponding value if Key appears in module flags, otherwisereturn null.
        """

    def add_flag(self, behavior: ModuleFlagBehavior, key: str, val: Metadata) -> None:
        """
        Add a module-level flag to the module-level flags metadata if it doesn'talready exist.
        """

    def dump(self) -> None:
        """Dump a representation of a module to stderr."""

    def print_to_file(self, filename: str) -> None:
        """
        Print a representation of a module to a file.
        :raises RuntimeError
        """

    def append_inline_asm(self, arg: str, /) -> None: ...

    def get_type_by_name(self, name: str = '') -> Type:
        """Deprecated: Use LLVMGetTypeByName2 instead."""

class ModuleFlagBehavior(enum.Enum):
    """ModuleFlagBehavior"""

    Error = 0
    """
    Adds a requirement that another module flag be present and have a specified value after linking is performed. The value must be a metadata pair, where the first element of the pair is the ID of the module flag to be restricted, and the second element of the pair is the value the module flag should be restricted to. This behavior can be used to restrict the allowable results (via triggering of an error) of linking IDs with the **Override** behavior.
    """

    Warning = 1
    """
    Emits a warning if two values disagree. The result value will be the operand for the flag from the first module being linked.
    """

    Require = 2
    """
    Adds a requirement that another module flag be present and have a specified value after linking is performed. The value must be a metadata pair, where the first element of the pair is the ID of the module flag to be restricted, and the second element of the pair is the value the module flag should be restricted to. This behavior can be used to restrict the allowable results (via triggering of an error) of linking IDs with the **Override** behavior.
    """

    Override = 3
    """
    Uses the specified value, regardless of the behavior or value of the other module. If both modules specify **Override**, but the values differ, an error will be emitted.
    """

    Append = 4
    """Appends the two values, which are required to be metadata nodes."""

    AppendUnique = 5
    """
    Appends the two values, which are required to be metadata nodes. However, duplicate entries in the second list are dropped during the append operation.
    """

class ModuleFlagEntry(llvmpym_ext.PymModuleFlagEntriesObject):
    """ModuleFlagEntry"""

    def __repr__(self) -> str: ...

    def get_behavior(self, index: int) -> ModuleFlagBehavior:
        """Returns the flag behavior for a module flag entry at a specific index."""

    def get_key(self, index: int) -> str:
        """Returns the key for a module flag entry at a specific index."""

    def get_metadata(self, index: int) -> Metadata:
        """Returns the metadata for a module flag entry at a specific index."""

class ModuleProvider(llvmpym_ext.PymModuleProviderObject):
    """ModuleProvider"""

    def __repr__(self) -> str: ...

    def create_function_pass_manager(self) -> FunctionPassManager:
        """Deprecated: Use :func:`Module.create_function_pass_manager` instead."""

class NamedMDNode(llvmpym_ext.PymNamedMDNodeObject):
    """NamedMDNode"""

    def __repr__(self) -> str: ...

    @property
    def next(self) -> NamedMDNode | None:
        """
        Advance a NamedMDNode iterator to the next NamedMDNode.

        Returns NULL if the iterator was already at the end and there are no more named metadata nodes.
        """

    @property
    def prev(self) -> NamedMDNode | None:
        """
        Decrement a NamedMDNode iterator to the previous NamedMDNode.

        Returns NULL if the iterator was already at the beginning and there areno previous named metadata nodes.
        """

    @property
    def name(self) -> str:
        """Retrieve the name of a NamedMDNode."""

class NamedMDNodeIterator:
    """NamedMDNodeIterator"""

    def __iter__(self) -> NamedMDNodeIterator: ...

    def __next__(self) -> NamedMDNode: ...

NoInfsFMFlag: int = 4

NoNaNsFMFlag: int = 2

NoSignedZerosFMFlag: int = 8

NoneFMFlag: int = 0

class Opcode(enum.Enum):
    """Opcode"""

    Ret = 1

    Br = 2

    Switch = 3

    IndirectBr = 4

    Invoke = 5

    Unreachable = 7

    CallBr = 67

    FNeg = 66

    Add = 8

    FAdd = 9

    Sub = 10

    FSub = 11

    Mul = 12

    FMul = 13

    UDiv = 14

    SDiv = 15

    FDiv = 16

    URem = 17

    SRem = 18

    FRem = 19

    Shl = 20

    LShr = 21

    AShr = 22

    And = 23

    Or = 24

    Xor = 25

    Alloca = 26

    Load = 27

    Store = 28

    GetElementPtr = 29

    Trunc = 30

    ZExt = 31

    SExt = 32

    FPToUI = 33

    FPToSI = 34

    UIToFP = 35

    SIToFP = 36

    FPTrunc = 37

    FPExt = 38

    PtrToInt = 39

    IntToPtr = 40

    BitCast = 41

    AddrSpaceCast = 60

    ICmp = 42

    FCmp = 43

    PHI = 44

    Call = 45

    Select = 46

    UserOp1 = 47

    UserOp2 = 48

    VAArg = 49

    ExtractElement = 50

    InsertElement = 51

    ShuffleVector = 52

    ExtractValue = 53

    InsertValue = 54

    Freeze = 68

    Fence = 55

    AtomicCmpXchg = 56

    AtomicRMW = 57

    Resume = 58

    LandingPad = 59

    CleanupRet = 61

    CatchRet = 62

    CatchPad = 63

    CleanupPad = 64

    CatchSwitch = 65

class OperandBundle(llvmpym_ext.PymOperandBundleObject):
    """OperandBundle"""

    def __init__(self, arg0: str, arg1: Sequence[Value], /) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def tag(self) -> str: ...

    @property
    def operands_num(self) -> int: ...

    def get_operand_at(self, arg: int, /) -> Value: ...

class PHINode(Instruction):
    """PHINode"""

    def __repr__(self) -> str: ...

    @property
    def incoming_num(self) -> int:
        """Obtain the number of incoming basic blocks to a PHI node."""

    def add_incoming(self, arg0: Sequence[Value], arg1: Sequence[BasicBlock], arg2: int, /) -> None: ...

    def get_incoming_value(self, arg: int, /) -> Value: ...

    def get_incoming_block(self, arg: int, /) -> BasicBlock: ...

class PassManager(PassManager):
    """PassManager"""

    def __init__(self) -> None:
        """
        Constructs a new whole-module pass pipeline. This type of pipeline issuitable for link-time optimization and whole-module transformations.
        """

    def __repr__(self) -> str: ...

    def run(self, module: Module) -> bool:
        """
        Initializes, executes on the provided module, and finalizes all of thepasses scheduled in the pass manager. Returns true if any of the passesmodified the module, false otherwise.
        """

class PointerType(SequenceType):
    """PointerType"""

    @overload
    def __init__(self, context: Context, address_space: int) -> None:
        """Create an opaque pointer type in a context."""

    @overload
    def __init__(self, elem_type: Type, address_space: int) -> None:
        """
        Create a pointer type that points to a defined type.

        The created type will exist in the context that its pointee typeexists in.
        """

    def __repr__(self) -> str: ...

    @property
    def is_opaque(self) -> int: ...

    @property
    def address_space(self) -> int: ...

class PoisonValue(Constant):
    """PoisonValue"""

    def __init__(self, type: Type) -> None:
        """Obtain a constant value referring to a poison value of a type."""

    def __repr__(self) -> str: ...

class RealPredicate(enum.Enum):
    """RealPredicate"""

    OEQ = 1
    """True if ordered and equal"""

    OGT = 2
    """True if ordered and greater than"""

    OGE = 3
    """True if ordered and greater than or equal"""

    OLT = 4
    """True if ordered and less than"""

    OLE = 5
    """True if ordered and less than or equal"""

    ONE = 6
    """True if ordered and operands are unequal"""

    ORD = 7
    """True if ordered (no nans)"""

    UNO = 8
    """True if unordered: isnan(X) | isnan(Y)"""

    UEQ = 9
    """True if unordered or equal"""

    UGT = 10
    """True if unordered or greater than"""

    UGE = 11
    """True if unordered, greater than, or equal"""

    ULT = 12
    """True if unordered or less than"""

    ULE = 13
    """True if unordered, less than, or equal"""

    UNE = 14
    """True if unordered or not equal"""

class RealType(Type):
    """RealType"""

    def __repr__(self) -> str: ...

    @staticmethod
    def Half(context: Context) -> RealType: ...

    @staticmethod
    def Bfloat(context: Context) -> RealType: ...

    @staticmethod
    def Float(context: Context) -> RealType: ...

    @staticmethod
    def Double(context: Context) -> RealType: ...

    @staticmethod
    def X86FP80(context: Context) -> RealType: ...

    @staticmethod
    def FP128(context: Context) -> RealType: ...

    @staticmethod
    def PPCFP128(context: Context) -> RealType: ...

    GlobalHalf: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalBfloat: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalFloat: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalDouble: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalX86FP80: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalFP128: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

    GlobalPPCFP128: llvmpym_ext.core.RealType = ...
    """Get type from global context."""

ReturnAttributeIndex: int = 0

class ReturnInst(Instruction):
    """ReturnInst"""

class SequenceType(Type):
    """SequenceType"""

    def __repr__(self) -> str: ...

    @property
    def element_type(self) -> Type: ...

class ShuffleVectorInst(Instruction):
    """ShuffleVectorInst"""

    def __repr__(self) -> str: ...

    @property
    def mask_elems_num(self) -> int: ...

    @staticmethod
    def get_undef_mask_elem(arg: ShuffleVectorInst, /) -> int:
        """
        returns a constant that specifies that the result of a ShuffleVectorInst is undefined.
        """

    def get_mask_value(self, index: int) -> int:
        """
        Get the mask value at position index in the mask of the ShuffleVectorinstruction.

        Returns the result of LLVMGetUndefMaskElem() if the mask value ispoison at that position.
        """

class StoreInst(Instruction):
    """StoreInst"""

    def __repr__(self) -> str: ...

    @property
    def alignment(self) -> int: ...

    @alignment.setter
    def alignment(self, bytes: int, /) -> None: ...

    @property
    def is_volatile(self) -> bool: ...

    @is_volatile.setter
    def is_volatile(self, arg: bool, /) -> None: ...

    @property
    def ordering(self) -> AtomicOrdering: ...

    @ordering.setter
    def ordering(self, arg: AtomicOrdering, /) -> None: ...

    @property
    def is_single_thread(self) -> bool: ...

    @is_single_thread.setter
    def is_single_thread(self, arg: bool, /) -> None: ...

class StringAttribute(Attribute):
    """StringAttribute"""

    def __init__(self, context: Context, kind: str, value: str) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def kind(self) -> str: ...

    @property
    def value(self) -> str:
        """Get the type attribute's value."""

class StructType(Type):
    """StructType"""

    @overload
    def __init__(self, context: Context, element_types: Sequence[Type], packed: bool) -> None:
        """Create a new structure type in context."""

    @overload
    def __init__(self, context: Context, name: str = '') -> None:
        """Create an empty structure in the context having a specified name."""

    def __repr__(self) -> str: ...

    @staticmethod
    def Global(element_types: Sequence[Type], packed: bool) -> StructType:
        """Create a new structure type in the global context."""

    @property
    def name(self) -> str: ...

    @property
    def elem_number(self) -> int: ...

    @property
    def elem_types(self) -> list[StructType]: ...

    @property
    def is_packed(self) -> bool:
        """Determine whether a structure is packed."""

    @property
    def is_opaque(self) -> bool: ...

    @property
    def is_literal(self) -> bool:
        """Determine whether a structure is literal."""

    def set_body(self, elem_types: Sequence[Type], packed: bool) -> None:
        """Set the contents of a structure type."""

    def get_type_at_index(self, index: int) -> Type | None:
        """Get the type of the element at a given index in the structure."""

class SwitchInst(Instruction):
    """SwitchInst"""

    def __repr__(self) -> str: ...

    @property
    def default_dest(self) -> BasicBlock: ...

    @property
    def add_case(self, arg0: ConstantInt, arg1: BasicBlock, /) -> None: ...

class TailCallKind(enum.Enum):
    """TailCallKind"""

    LLVMTailCallKindNone = 0

    LLVMTailCallKindTail = 1

    LLVMTailCallKindMustTail = 2

    LLVMTailCallKindNoTail = 3

class TargetExtType(Type):
    """TargetExtType"""

    def __init__(self, arg0: Context, arg1: str, arg2: Sequence[Type], arg3: Sequence[int], /) -> None: ...

    def __repr__(self) -> str: ...

class ThreadLocalMode(enum.Enum):
    """ThreadLocalMode"""

    NotThreadLocal = 0

    GeneralDynamic = 1

    LocalDynamic = 2

    InitialExec = 3

    LocalExec = 4

class TokenType(Type):
    """TokenType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

class Type(llvmpym_ext.PymTypeObject):
    """Type"""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    @property
    def align(self) -> ConstantExpr: ...

    @property
    def size(self) -> ConstantExpr: ...

    @property
    def kind(self) -> TypeKind:
        """Obtain the enumerated type of a Type instance."""

    @property
    def is_sized(self) -> bool:
        """
        Whether the type has a known size.

        Things that don't have a size are abstract types, labels, and void.a
        """

    @property
    def context(self) -> Context:
        """Obtain the context to which this type instance is associated."""

    @property
    def sub_type_number(self) -> int: ...

    @property
    def sub_types(self) -> list[SequenceType]: ...

    def null(self) -> Value:
        """Obtain a constant value referring to the null instance of the type."""

    def pointer_null(self) -> Value:
        """
        Obtain a constant that is a constant pointer pointing to NULL for thetype.
        """

    def undef(self) -> UndefValue:
        """Obtain a constant value referring to an undefined value of a type."""

    def poison(self) -> PoisonValue:
        """Obtain a constant value referring to a poison value of a type."""

    def dump(self) -> None:
        """Dump a representation of a type to stderr."""

class TypeAttribute(Attribute):
    """TypeAttribute"""

    def __init__(self, context: Context, kind_id: int, type: Type) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def value(self) -> Type:
        """Get the type attribute's value."""

class TypeKind(enum.Enum):
    """TypeKind"""

    Void = 0
    """type with no size"""

    Half = 1
    """16 bit floating point type"""

    Float = 2
    """32 bit floating point type"""

    Double = 3
    """64 bit floating point type"""

    X86_FP80 = 4
    """80 bit floating point type (X87)"""

    FP128 = 5
    """128 bit floating point type (112-bit mantissa)"""

    PPC_FP128 = 6
    """128 bit floating point type (two 64-bits)"""

    Label = 7
    """Labels"""

    Integer = 8
    """Arbitrary bit width integers"""

    Function = 9
    """Functions"""

    Struct = 10
    """Structures"""

    Array = 11
    """Arrays"""

    Pointer = 12
    """Pointers"""

    Vector = 13
    """Fixed width SIMD vector type"""

    Metadata = 14
    """Metadata"""

    X86_MMX = 15
    """X86 MMX"""

    Token = 16
    """Tokens"""

    ScalableVector = 17
    """Scalable SIMD vector type"""

    BFloat = 18
    """16 bit brain floating point type"""

    X86_AMX = 19
    """X86 AMX"""

    TargetExt = 20
    """Target extension type"""

class UndefValue(Constant):
    """UndefValue"""

    def __init__(self, type: Type) -> None:
        """Obtain a constant value referring to an undefined value of a type."""

    def __repr__(self) -> str: ...

class UnnamedAddr(enum.Enum):
    """UnnamedAddr"""

    No = 0
    """Address of the GV is significant."""

    Local = 1
    """Address of the GV is locally insignificant."""

    Global = 2
    """Address of the GV is globally insignificant."""

class Use(llvmpym_ext.PymUseObject):
    """Use"""

    def __repr__(self) -> str: ...

    @property
    def next(self) -> Use | None:
        """
        Obtain the next use of a value.

        This effectively advances the iterator. It returns NULL if you are onthe final use and no more are available.
        """

    @property
    def user(self) -> Value:
        """The returned value corresponds to a llvm::User type."""

    @property
    def used_value(self) -> Value: ...

class UseIterator:
    """UseIterator"""

    def __iter__(self) -> UseIterator: ...

    def __next__(self) -> Use: ...

class User(Value):
    """User"""

    def __repr__(self) -> str: ...

    @property
    def operands_num(self) -> int: ...

    @property
    def operands(self) -> list[Value]: ...

    def get_operand(self, index: int) -> Value:
        """Obtain an operand at a specific index."""

    def get_operand_use(self, arg: int, /) -> Use:
        """Obtain the use of an operand at a specific index"""

    def set_operand(self, index: int, value: Value) -> None:
        """Set an operand at a specific index"""

class Value(llvmpym_ext.PymValueObject):
    """Value"""

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    @property
    def type(self) -> Type: ...

    @property
    def kind(self) -> ValueKind: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def is_constant(self) -> bool: ...

    @property
    def is_undef(self) -> bool: ...

    @property
    def is_poisonous(self) -> bool: ...

    @property
    def first_use(self) -> Use | None: ...

    @property
    def uses(self) -> UseIterator: ...

    def as_metadata(self) -> ValueAsMetadata: ...

    def dump(self) -> None:
        """Dump a representation of a value to stderr."""

    @staticmethod
    def replace_all_uses_with(arg0: Value, arg1: Value, /) -> None:
        """Replace all uses of a value with another one."""

    def to_Argument(self) -> Value | None:
        """
        Origin function: LLVMIsAArgument

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_InlineAsm(self) -> Value | None:
        """
        Origin function: LLVMIsAInlineAsm

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_User(self) -> Value | None:
        """
        Origin function: LLVMIsAUser

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_Constant(self) -> Value | None:
        """
        Origin function: LLVMIsAConstant

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_BlockAddress(self) -> Value | None:
        """
        Origin function: LLVMIsABlockAddress

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantAggregateZero(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantAggregateZero

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantArray(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantArray

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantDataSequential(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantDataSequential

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantDataArray(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantDataArray

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantDataVector(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantDataVector

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantExpr(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantExpr

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantFP(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantFP

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantInt(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantInt

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantPointerNull(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantPointerNull

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantStruct(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantStruct

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantTokenNone(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantTokenNone

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ConstantVector(self) -> Value | None:
        """
        Origin function: LLVMIsAConstantVector

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GlobalValue(self) -> Value | None:
        """
        Origin function: LLVMIsAGlobalValue

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GlobalAlias(self) -> Value | None:
        """
        Origin function: LLVMIsAGlobalAlias

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GlobalObject(self) -> Value | None:
        """
        Origin function: LLVMIsAGlobalObject

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_Function(self) -> Value | None:
        """
        Origin function: LLVMIsAFunction

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GlobalVariable(self) -> Value | None:
        """
        Origin function: LLVMIsAGlobalVariable

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GlobalIFunc(self) -> Value | None:
        """
        Origin function: LLVMIsAGlobalIFunc

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_UndefValue(self) -> Value | None:
        """
        Origin function: LLVMIsAUndefValue

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_PoisonValue(self) -> Value | None:
        """
        Origin function: LLVMIsAPoisonValue

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_Instruction(self) -> Value | None:
        """
        Origin function: LLVMIsAInstruction

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_UnaryOperator(self) -> Value | None:
        """
        Origin function: LLVMIsAUnaryOperator

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_BinaryOperator(self) -> Value | None:
        """
        Origin function: LLVMIsABinaryOperator

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CallInst(self) -> Value | None:
        """
        Origin function: LLVMIsACallInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_IntrinsicInst(self) -> Value | None:
        """
        Origin function: LLVMIsAIntrinsicInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_DbgInfoIntrinsic(self) -> Value | None:
        """
        Origin function: LLVMIsADbgInfoIntrinsic

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_DbgVariableIntrinsic(self) -> Value | None:
        """
        Origin function: LLVMIsADbgVariableIntrinsic

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_DbgDeclareInst(self) -> Value | None:
        """
        Origin function: LLVMIsADbgDeclareInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_DbgLabelInst(self) -> Value | None:
        """
        Origin function: LLVMIsADbgLabelInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_MemIntrinsic(self) -> Value | None:
        """
        Origin function: LLVMIsAMemIntrinsic

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_MemCpyInst(self) -> Value | None:
        """
        Origin function: LLVMIsAMemCpyInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_MemMoveInst(self) -> Value | None:
        """
        Origin function: LLVMIsAMemMoveInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_MemSetInst(self) -> Value | None:
        """
        Origin function: LLVMIsAMemSetInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CmpInst(self) -> Value | None:
        """
        Origin function: LLVMIsACmpInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FCmpInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFCmpInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ICmpInst(self) -> Value | None:
        """
        Origin function: LLVMIsAICmpInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ExtractElementInst(self) -> Value | None:
        """
        Origin function: LLVMIsAExtractElementInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_GetElementPtrInst(self) -> Value | None:
        """
        Origin function: LLVMIsAGetElementPtrInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_InsertElementInst(self) -> Value | None:
        """
        Origin function: LLVMIsAInsertElementInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_InsertValueInst(self) -> Value | None:
        """
        Origin function: LLVMIsAInsertValueInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_LandingPadInst(self) -> Value | None:
        """
        Origin function: LLVMIsALandingPadInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_PHINode(self) -> Value | None:
        """
        Origin function: LLVMIsAPHINode

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_SelectInst(self) -> Value | None:
        """
        Origin function: LLVMIsASelectInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ShuffleVectorInst(self) -> Value | None:
        """
        Origin function: LLVMIsAShuffleVectorInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_StoreInst(self) -> Value | None:
        """
        Origin function: LLVMIsAStoreInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_BranchInst(self) -> Value | None:
        """
        Origin function: LLVMIsABranchInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_IndirectBrInst(self) -> Value | None:
        """
        Origin function: LLVMIsAIndirectBrInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_InvokeInst(self) -> Value | None:
        """
        Origin function: LLVMIsAInvokeInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ReturnInst(self) -> Value | None:
        """
        Origin function: LLVMIsAReturnInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_SwitchInst(self) -> Value | None:
        """
        Origin function: LLVMIsASwitchInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_UnreachableInst(self) -> Value | None:
        """
        Origin function: LLVMIsAUnreachableInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ResumeInst(self) -> Value | None:
        """
        Origin function: LLVMIsAResumeInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CleanupReturnInst(self) -> Value | None:
        """
        Origin function: LLVMIsACleanupReturnInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CatchReturnInst(self) -> Value | None:
        """
        Origin function: LLVMIsACatchReturnInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CatchSwitchInst(self) -> Value | None:
        """
        Origin function: LLVMIsACatchSwitchInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CallBrInst(self) -> Value | None:
        """
        Origin function: LLVMIsACallBrInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FuncletPadInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFuncletPadInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CatchPadInst(self) -> Value | None:
        """
        Origin function: LLVMIsACatchPadInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CleanupPadInst(self) -> Value | None:
        """
        Origin function: LLVMIsACleanupPadInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_UnaryInstruction(self) -> Value | None:
        """
        Origin function: LLVMIsAUnaryInstruction

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_AllocaInst(self) -> Value | None:
        """
        Origin function: LLVMIsAAllocaInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_CastInst(self) -> Value | None:
        """
        Origin function: LLVMIsACastInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_AddrSpaceCastInst(self) -> Value | None:
        """
        Origin function: LLVMIsAAddrSpaceCastInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_BitCastInst(self) -> Value | None:
        """
        Origin function: LLVMIsABitCastInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FPExtInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFPExtInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FPToSIInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFPToSIInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FPToUIInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFPToUIInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FPTruncInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFPTruncInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_IntToPtrInst(self) -> Value | None:
        """
        Origin function: LLVMIsAIntToPtrInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_PtrToIntInst(self) -> Value | None:
        """
        Origin function: LLVMIsAPtrToIntInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_SExtInst(self) -> Value | None:
        """
        Origin function: LLVMIsASExtInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_SIToFPInst(self) -> Value | None:
        """
        Origin function: LLVMIsASIToFPInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_TruncInst(self) -> Value | None:
        """
        Origin function: LLVMIsATruncInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_UIToFPInst(self) -> Value | None:
        """
        Origin function: LLVMIsAUIToFPInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ZExtInst(self) -> Value | None:
        """
        Origin function: LLVMIsAZExtInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_ExtractValueInst(self) -> Value | None:
        """
        Origin function: LLVMIsAExtractValueInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_LoadInst(self) -> Value | None:
        """
        Origin function: LLVMIsALoadInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_VAArgInst(self) -> Value | None:
        """
        Origin function: LLVMIsAVAArgInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FreezeInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFreezeInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_AtomicCmpXchgInst(self) -> Value | None:
        """
        Origin function: LLVMIsAAtomicCmpXchgInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_AtomicRMWInst(self) -> Value | None:
        """
        Origin function: LLVMIsAAtomicRMWInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_FenceInst(self) -> Value | None:
        """
        Origin function: LLVMIsAFenceInst

        None means conversion failed.

        Note if the target class is not supported in python binding, then it will return a generic PymValue type object
        """

    def to_BasicBlockValue(self) -> BasicBlockValue | None: ...

    def to_MDNodeValue(self) -> MDNodeValue | None: ...

    def to_ValueAsMetadataValue(self) -> ValueAsMetadataValue | None: ...

    def to_MDStringValue(self) -> MDStringValue | None: ...

    @property
    def is_basic_block(self) -> bool: ...

    def as_basic_block(self) -> BasicBlock: ...

class ValueAsMetadata(Metadata):
    """ValueAsMetadata"""

class ValueAsMetadataValue(MetadataAsValue):
    """ValueAsMetadataValue"""

class ValueKind(enum.Enum):
    """ValueKind"""

    Argument = 0

    BasicBlock = 1

    MemoryUse = 2

    MemoryDef = 3

    MemoryPhi = 4

    Function = 5

    GlobalAlias = 6

    GlobalIFunc = 7

    GlobalVariable = 8

    BlockAddress = 9

    ConstantExpr = 10

    ConstantArray = 11

    ConstantStruct = 12

    ConstantVector = 13

    UndefValue = 14

    ConstantAggregateZero = 15

    ConstantDataArray = 16

    ConstantDataVector = 17

    ConstantInt = 18

    ConstantFP = 19

    ConstantPointerNull = 20

    ConstantTokenNone = 21

    MetadataAsValue = 22

    InlineAsm = 23

    Instruction = 24

    PoisonValue = 25

    ConstantTargetNone = 26

class VectorType(SequenceType):
    """VectorType"""

    def __init__(self, elem_type: Type, elem_count: int, is_scalable: bool) -> None:
        """
        The created type will exist in the context thats its element typeexists in.
        """

    def __repr__(self) -> str: ...

    __len__: int = ...
    """(arg: llvmpym_ext.core.VectorType, /) -> int"""

class Visibility(enum.Enum):
    """Visibility"""

    Default = 0
    """The GV is visible"""

    Hidden = 1
    """The GV is hidden"""

    Protected = 2
    """The GV is protected"""

class VoidType(Type):
    """VoidType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

    Global: llvmpym_ext.core.VoidType = ...
    """(arg: object, /) -> llvmpym_ext.core.VoidType"""

class X86AMXType(Type):
    """X86AMXType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

    Global: llvmpym_ext.core.X86AMXType = ...
    """(arg: object, /) -> llvmpym_ext.core.X86AMXType"""

class X86MMXType(Type):
    """X86MMXType"""

    def __init__(self, context: Context) -> None: ...

    def __repr__(self) -> str: ...

    Global: llvmpym_ext.core.X86MMXType = ...
    """(arg: object, /) -> llvmpym_ext.core.X86MMXType"""

def get_version() -> "std::__1::tuple<unsigned int, unsigned int, unsigned int>":
    """
    Return the major, minor, and patch version of LLVM
    The version components are returned via the function's three output parameters or skipped if a NULL pointer was supplied.
    """

def llvm_is_multithreaded() -> bool: ...

def shutdown() -> None:
    """Deallocate and destroy all ManagedStatic variables."""
