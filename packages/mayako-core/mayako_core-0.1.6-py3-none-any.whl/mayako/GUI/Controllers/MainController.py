from ..Views.MainView import MainView
from .AddDeviceController import AddDeviceController
from .DeviceDetailsController import DeviceDetailsController
from .AddWiFiProfileController import AddWiFiProfileController
from .EditWiFiProfileController import EditWiFiProfileController
from .DownloadArduinoController import DownloadArduinoController
from .HomeController import HomeController
from ...MayakoData import MayakoData
from ...Client import Client

class MainController:

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.model = model
        self.main_view = main_view
        self.client = client
        self.home_controller = HomeController(self.main_view, self.model, self.client)
        self.add_device_controller = AddDeviceController(self.main_view, self.model, self.client)
        self.add_wifi_profile_controller = AddWiFiProfileController(self.main_view, self.model, self.client)
        self.edit_wifi_profile_controller = EditWiFiProfileController(self.main_view, self.model, self.client)
        self.device_deails_controller = DeviceDetailsController(self.main_view, self.model, self.client)
        self.download_arduino_controller = DownloadArduinoController(self.main_view, self.model, self.client)

    def start(self) -> None:
        self.main_view.switch("home")
        self.main_view.start_mainloop()

