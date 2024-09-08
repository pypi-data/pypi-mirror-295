import inspect
from ..settings import settings

def simple_test() -> None:
    """
    Run a basic check to verify the function is working correctly.
    """
    # Retrieve the current frame and the line number of the caller
    frame = inspect.currentframe()
    caller_frame = frame.f_back         #type:ignore
    line_number = caller_frame.f_lineno #type:ignore
    
    green: str = settings.GREEN
    reset: str = settings.RESET
    
    # Print a message with green color to indicate success, including the line number
    print(f"{green}^_^ Everything seems to be working here! (Line: {line_number}){reset}")