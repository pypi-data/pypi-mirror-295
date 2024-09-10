import socket
import psutil  #type:ignore

def get_local_ip() -> str:
    """
    Gets the local IP on a Windows computer.

    :return ip (str): The IP.
    """
    # Check both Ethernet and Wi-Fi interfaces
    for interface in ['Ethernet', 'WiFi']:
        ip_addresses = [addr.address for addr in psutil.net_if_addrs().get(interface, []) if addr.family == socket.AF_INET]
        if ip_addresses:
            return ip_addresses[0]
        
    raise ValueError("No local IP found")

# Test
if __name__ == "__main__":
    print(get_local_ip())