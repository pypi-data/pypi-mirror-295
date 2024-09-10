import uuid

def get_macaddress() -> str:
    """
    returns the macaddress of the underlying computer.
    
    this function returns the macaddress of the underlying computer. it uses the uuid standard library package. the format is e.g. 02:73:ab:ab:0e:e7. it returns all 1 if no mac address was found.

    References:
        https://stackoverflow.com/a/28928058

    Returns:
        mac (str):
            Example: 02:73:ab:ab:0e:e7
    """
    address_as_int = uuid.getnode()
    h = iter(hex(address_as_int)[2:].zfill(12))
    mac = ":".join(i + next(h) for i in h)

    return mac