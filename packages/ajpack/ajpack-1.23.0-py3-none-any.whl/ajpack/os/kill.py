import psutil

def kill_process(pid: int):
    """
    Terminates a process by its PID. Use aj.list_processes() to get the pid of a process.

    :param pid: Pid to terminate.
    """
    psutil.Process(pid).terminate()