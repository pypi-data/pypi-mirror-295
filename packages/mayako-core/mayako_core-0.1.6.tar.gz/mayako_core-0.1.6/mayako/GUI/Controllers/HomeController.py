import tkinter as tk
from tkinter import messagebox
from typing import List

from ..Views.MainView import MainView
from ..Views.HomeView import HomeView
from ...MayakoData import MayakoData
from ...Client import Client

class HomeController:

    main_view: MainView
    home_frame: HomeView

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.model = model
        self.main_view = main_view
        self.client = client
        self.home_frame = self.main_view.frame_classes["home"]

        self._load_wifi_profiles_into_list()
        self._load_microcontrollers_into_list()
        self._view_bind()
        self._model_subscribe()

        for mc in self.model.get_microcontroller_capas():
            self.client.use_microcontroller(mc.identity)

    def _load_wifi_profiles_into_list(self) -> None:
        for key, profile in enumerate(self.model.get_wifi_profiles()):
            self.home_frame.wifi_listbox.insert(key, profile.format_string())

    def _load_microcontrollers_into_list(self) -> None:
        for key, microcontroller in enumerate(self.model.get_microcontroller_capas()):
            self.home_frame.devices_listbox.insert(key, microcontroller.format_string())

    def _view_bind(self) -> None:
        #devices
        self.home_frame.get_arduino_btn.config(command=self._change_frame_to_download_arduino)
        self.home_frame.add_device_btn.config(command=self._add_new_device)
        self.home_frame.remove_device_btn.config(command=self._remove_device)
        self.home_frame.device_details_btn.config(command=self._change_frame_to_device_details)

        #wifi profiles
        self.home_frame.add_wifi_btn.config(command=self._add_new_wifi_profile)
        self.home_frame.remove_wifi_btn.config(command=self._remove_wifi_profile)
        self.home_frame.wifi_details_btn.config(command=self._change_frame_to_wifi_profile_details)

    def _model_subscribe(self) -> None:
        self.model.subscribe("wifi_profiles_update", self._update_wifi_profiles)
        self.model.subscribe("microcontroller_capa_update", self._update_microcontrollers)

    def _update_wifi_profiles(self, _) -> None:
        self.home_frame.wifi_listbox.delete(0, tk.END)

        self._load_wifi_profiles_into_list()

    def _update_microcontrollers(self, _) -> None:
        self.home_frame.devices_listbox.delete(0, tk.END)

        self._load_microcontrollers_into_list()

    #download arduino frame
    def _change_frame_to_download_arduino(self) -> None:
        self.main_view.switch("download")

    #devices
    def _add_new_device(self) -> None:
        self.main_view.switch("add_device")

    def _remove_device(self) -> None:
        selected_item = self.home_frame.devices_listbox.curselection()

        if selected_item:
            item = self.model.get_microcontroller_capas()[selected_item[0]]
            self.model.remove_microcontroller_capa(item)

        else:
            messagebox.showerror(title="Error", message="no item selected")

    def _change_frame_to_device_details(self) -> None:
        selected_item = self.home_frame.devices_listbox.curselection()

        if selected_item:
            self.main_view.switch("device_details")
            self.model.select_microcontroller_capa(self.model.get_microcontroller_capas()[selected_item[0]])
    
        else:
            messagebox.showerror(title="Error", message="select an item to view")

    #wifi profiles
    def _add_new_wifi_profile(self) -> None:
        self.main_view.switch("add_wifi")

    def _remove_wifi_profile(self) -> None:
        selected_item = self.home_frame.wifi_listbox.curselection()

        if selected_item:
            item = self.model.get_wifi_profiles()[selected_item[0]]
            self.model.remove_wifi_profile(item)
        else:
            messagebox.showerror(title="Error", message="no item selected")

    def _change_frame_to_wifi_profile_details(self) -> None:
        selected_item = self.home_frame.wifi_listbox.curselection()

        if selected_item:
            self.main_view.switch("edit_wifi")
            self.model.select_wifi_profile(self.model.get_wifi_profiles()[selected_item[0]])
        else:
            messagebox.showerror(title="Error", message="select an item to view")