import psutil  #type:ignore
import time

def get_system_uptime() -> float:
    """
    This function returns the system uptime in seconds.

    :return uptime (float): The uptime in seconds.
    """
    
    # Get the system boot time
    boot_time = psutil.boot_time()
    
    # Calculate the system uptime by subtracting the boot time from the current time
    uptime = time.time() - boot_time
    
    return uptime

# Test
if __name__ == "__main__":
    print(f"System uptime: {get_system_uptime()} seconds")