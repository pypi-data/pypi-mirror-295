from collections.abc import Callable


def enable_pretty_stack_trace() -> None:
    """
    Enable LLVM's built-in stack trace code. This intercepts the OS's crashsignals and prints which component of LLVM you were in at the time if thecrash.
    """

def install_fatal_error_handler(handler: Callable[[str], None]) -> None:
    """
    Install a fatal error handler. By default, if LLVM detects a fatal error, itwill call exit(1). This may not be appropriate in many contexts. For example,doing exit(1) will bypass many crash reporting/tracing system tools. Thisfunction allows you to install a callback that will be invoked prior to thecall to exit(1).
    """

def reset_fatal_error_handler() -> None:
    """
    Reset the fatal error handler. This resets LLVM's fatal error handlingbehavior to the default.
    """
