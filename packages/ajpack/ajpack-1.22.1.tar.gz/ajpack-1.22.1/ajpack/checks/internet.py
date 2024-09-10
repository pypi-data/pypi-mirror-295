import socket, os

def has_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
    """
    Checks if the internet connection is available.
    
    :param host: The target ip.
    :param port: The target port.
    :param timeout: How long to wait if no response.
    :return: If connection to the target.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def ping(target_ip: str) -> bool:
    """
    Pings a target IP address.
    
    :param target_ip: The target ip.
    :return: If connection to the target.
    """
    response: int = os.system("ping -c 1" + target_ip)
    return response == 0

def check_open_port(host_ip: str, port: int, timeout: float = 5) -> bool:
    """
    Checks if a specific port is opened on the host ip.
    
    :param host_ip: Target ip.
    :param port: Target port.
    :param timeout: How long to wait if no response.
    :return: If port is open.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host_ip, port))
        return result == 0