from dataclasses import dataclass, asdict
from typing import Self, Dict

@dataclass
class WiFiProfile:
    """
    the is the model class for wifi profiles

    the wifi profile is setup in the GUI and can be appended as a build flag when flashing the arduino board using wireless_mode WIFI.

    Attributes:
        wifi_key (str): a short identity for a wifi profile; must be unique
        ssid (str): the address of the wifi router
        password (str): the password the accesses the wifi
        client_ip (str): the IP of the client application available by the router and thereby from the microcontroller
        client_port (int): the bound port on the clients machine to access the socket
    
    """

    wifi_key: str
    ssid: str
    password: str
    client_ip: str
    client_port: int

    def format_string(self) -> str:
        """
        this method formats a string from selected properties of the class to return a string that can be displayed in the GUI

        Returns:
            (str): a string describing the wifi profile
        """
        return f"WiFi Key: {self.wifi_key} -- SSID: {self.ssid} -- client IP: {self.client_ip} -- client Port: {self.client_port}"
    
    def to_dict(self) -> Dict:
        """
        returns the wifi profile as a Dict

        Returns:
            (Dict): wifi profile as dict
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """
        converts a dictionary to a class of the according type

        This is a classmethod which converts a dictionary that contains all class properties into an instance of the according type. the dictionary can contain properties that are not fitting in the class; theses properties will be ignored. This is helpful to filter out information that is not part of this class.

        Sources:
            https://stackoverflow.com/a/73264198
            https://stackoverflow.com/a/54769644

        Args:
            data (Dict): a dictionary that contains all properties of this class and more

        Returns:
            Self: return an instance of the class that contains the values from the dictionary

        """
        return cls(**data)