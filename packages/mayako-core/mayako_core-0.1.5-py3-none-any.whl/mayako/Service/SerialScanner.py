from serial.tools.list_ports import comports
from typing import List
from ..Models.SerialInfo import SerialInfo

def scan_serial_ports(device_names: List[str]) -> List[SerialInfo]:
    """
    This function scans all serial ports on the machine (WIN, MACOS, LINUX). Arduino boards often have a description containing the name of the USB-to-UART bridge controller. Therefore we can filter the scanned ports by looking for keywords defined in Config.h > CNETWORK > SERIAL_ARDUINO_WORDS. We stored following information in a dataclass: the port of the found arduino board, the serial number to identify the board in another iteration, the description which contains the keywords.

    Source:
        https://github.com/pyserial/pyserial

    Args:
        device_names (List[str]):
            a list of words that are typical for the arduino serial port description

    Returns:
        list of ports which match our criteria for an arduino board
    """
    available_ports = comports()
    arduino_ports: List[SerialInfo] = []

    for port in available_ports:
        if len(device_names) != 0 and any(keyword in port.description for keyword in device_names):
            serial_number = getattr(port, "serial_number", "unknown")

            arduino_ports.append(SerialInfo(port.device, serial_number, port.description))

    return arduino_ports

if __name__ == "__main__":
    device_name = ["CP2104", "Arduino"]
    serial_ports = scan_serial_ports(device_name)