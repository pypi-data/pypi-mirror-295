import socket

def get_user_ip_address() -> int:
    """
    this function creates a socket, connects to a random ip address, reads the socket information that also contains the machines used ip address.

    Sources:
        https://stackoverflow.com/a/30990617

    Returns:
        int: the ip address of the machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip