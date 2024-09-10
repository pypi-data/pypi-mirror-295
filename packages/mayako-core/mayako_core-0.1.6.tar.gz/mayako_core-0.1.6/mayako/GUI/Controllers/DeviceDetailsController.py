import tkinter as tk
from tkinter import messagebox
import json
from ..Views.MainView import MainView
from ..Views.DeviceDetailsView import DeviceDetailsView
from ...MayakoData import MayakoData
from ...Client import Client

#TODO
from ...Models.Button import Button
from ...Models.Temperature import Temperature
from ...Models.SensorCapabilities import SensorCapabilities
from ...Models.ActuatorCapabilities import ActuatorCapabilities

class DeviceDetailsController:

    main_view: MainView
    device_details_frame: DeviceDetailsView

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.main_view = main_view
        self.model = model
        self.client = client
        self.device_details_frame = self.main_view.frame_classes["device_details"]
        self._bind()
        self._model_subscribe()

    def _bind(self) -> None:
        self.device_details_frame.return_btn.config(command=self._return_to_main)
        self.device_details_frame.update_capabilities_btn.config(command=self._update_capabilities)
        #self.device_details_frame.identify_device_btn.config(command=self._identify)

    def _return_to_main(self) -> None:
        self.main_view.switch("home")

    def _model_subscribe(self) -> None:
        self.model.subscribe("microcontroller_capa_selected", self._load_microcontroller)

    def _load_microcontroller(self, mayako_data: MayakoData) -> None:
        mc = mayako_data.selected_mc_capability
        self.device_details_frame.identity_text.config(text=mc.identity)
        self.device_details_frame.protocol_text.config(text=f"{mc.protocol.name} -- {"online" if mc.online else "offline"}")
        self.device_details_frame.battery_text.config(text=f"{mc.battery_percentage}% -- {'charging' if mc.battery_charging else 'running on battery'}")

        self.device_details_frame.capabilities_text.delete("1.0", tk.END)
        self.device_details_frame.capabilities_text.insert(tk.END, json.dumps(mc.to_dict(), indent=4))
        
    def _update_capabilities(self) -> None:
        mc_capa = self.model.selected_mc_capability
        #check if online => enable button
        
        try:
            #if mc_capa.identity not in self.client._microcontrollers:
            #    self.client.use_microcontroller(mc_identity=mc_capa.identity)
            self.client._commands.record_read(mc_identity=mc_capa.identity)

        except Exception as e:
            print(e)
            messagebox.showerror("ERROR", "device not available")

    """ def _identify(self) -> None:
        mc_capa = self.model.selected_mc_capability
        try:
            #if mc_capa.identity not in self.client._microcontrollers:
            #    self.client.use_microcontroller(mc_identity=mc_capa.identity)

            #self.client._commands.identify(mc_identity=mc_capa.identity, identity=mc_capa.identity)
            messagebox.showinfo("INFO", "this feature is not implemented.")
        except:
            messagebox.showerror("ERROR", "device not available") """