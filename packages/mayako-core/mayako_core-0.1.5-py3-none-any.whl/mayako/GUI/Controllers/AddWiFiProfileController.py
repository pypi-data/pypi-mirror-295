import tkinter as tk
from tkinter import messagebox

from ..Views.MainView import MainView
from ..Views.AddWiFiProfileView import AddWiFiProfileView
from ...Models.WiFiProfile import WiFiProfile
from ...MayakoData import MayakoData
from ...Client import Client

class AddWiFiProfileController:

    main_view: MainView
    add_wifi_frame: AddWiFiProfileView

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.main_view = main_view
        self.model = model
        self.client = client
        self.add_wifi_frame = self.main_view.frame_classes["add_wifi"]
        self._bind()

    def _bind(self) -> None:
        self.add_wifi_frame.return_btn.config(command=self._return_to_main)
        self.add_wifi_frame.add_wifi_profile_btn.config(command=self._add_wifi_profile)

    def _return_to_main(self) -> None:
        self.main_view.switch("home")
        self.add_wifi_frame.wifi_key_entry.delete(0, tk.END)
        self.add_wifi_frame.ssid_entry.delete(0, tk.END)
        self.add_wifi_frame.password_entry.delete(0, tk.END)
        self.add_wifi_frame.client_ip_entry.delete(0, tk.END)
        self.add_wifi_frame.client_port_entry.delete(0, tk.END)

    def _add_wifi_profile(self) -> None:
        wifi_key = self.add_wifi_frame.wifi_key_entry.get()
        ssid = self.add_wifi_frame.ssid_entry.get()
        password = self.add_wifi_frame.password_entry.get()
        client_ip = self.add_wifi_frame.client_ip_entry.get()
        client_port = self.add_wifi_frame.client_port_entry.get()

        if len(wifi_key) < 4:
            messagebox.showerror(title="Error", message="wifi key must be 4 characters long")
            return
        if self.model.get_wifi_profile_by_wifi_key(wifi_key=wifi_key):
            messagebox.showerror(title="Error", message="a wifi profile with this identity already exists. please use another wifi key.")
            return
        if ssid == "":
            messagebox.showerror(title="Error", message="ssid may not be empty")
            return
        if password == "":
            messagebox.showerror(title="Error", message="password may not be empty")
            return
        if client_ip == "":
            messagebox.showerror(title="Error", message="client ip may not be empty")
            return
        try:
            client_port = int(client_port)                
        except ValueError:
            messagebox.showerror(title="Error", message="client port must be an integer and may not be empty")
            return

        profile = WiFiProfile(
            wifi_key=wifi_key,
            ssid=ssid,
            password=password,
            client_ip=client_ip,
            client_port=client_port
            )
        
        self.model.add_wifi_profile([profile])

        self.main_view.switch("home")