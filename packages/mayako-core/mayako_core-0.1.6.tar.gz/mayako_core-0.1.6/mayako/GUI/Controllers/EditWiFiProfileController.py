import tkinter as tk
from ..Views.MainView import MainView
from ..Views.EditWiFiProfileView import EditWiFiProfileView
from ...MayakoData import MayakoData
from ...Models.WiFiProfile import WiFiProfile
from ...Client import Client

class EditWiFiProfileController:

    main_view: MainView
    edit_wifi_frame: EditWiFiProfileView

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.main_view = main_view
        self.model = model
        self.client = client
        self.edit_wifi_frame = self.main_view.frame_classes["edit_wifi"]
        self._bind()
        self._model_subscribe()

    def _bind(self) -> None:
        self.edit_wifi_frame.return_btn.config(command=self._return_to_main)
        self.edit_wifi_frame.edit_wifi_profile_btn.config(command=self._update_wifi_profile)

    def _return_to_main(self, *_) -> None:
        self.main_view.switch("home")

    def _model_subscribe(self) -> None:
        self.model.subscribe("wifi_profile_selected", self._load_wifi_profile)

    def _load_wifi_profile(self, mayako_data: MayakoData) -> None:
        wifi_profile = mayako_data.selected_wifi_profile
        
        self.edit_wifi_frame.wifi_key_entry.config(text=wifi_profile.wifi_key)

        self.edit_wifi_frame.ssid_entry.delete(0, tk.END)
        self.edit_wifi_frame.ssid_entry.insert(0, wifi_profile.ssid)

        self.edit_wifi_frame.password_entry.delete(0, tk.END)
        self.edit_wifi_frame.password_entry.insert(0, wifi_profile.password)

        self.edit_wifi_frame.client_ip_entry.delete(0, tk.END)
        self.edit_wifi_frame.client_ip_entry.insert(0, wifi_profile.client_ip)

        self.edit_wifi_frame.client_port_entry.delete(0, tk.END)
        self.edit_wifi_frame.client_port_entry.insert(0, wifi_profile.client_port)

    def _update_wifi_profile(self, *_) -> None:
        existing_wifi_key = self.model.selected_wifi_profile.wifi_key
        
        ssid = self.edit_wifi_frame.ssid_entry.get()
        password = self.edit_wifi_frame.password_entry.get()
        client_ip = self.edit_wifi_frame.client_ip_entry.get()
        client_port = int(self.edit_wifi_frame.client_port_entry.get())

        updated_wifi_profile = WiFiProfile(wifi_key=existing_wifi_key, ssid=ssid, password=password, client_ip=client_ip, client_port=client_port)

        self.model.update_wifi_profile(updated_wifi_profile)

        self.main_view.switch("home")
