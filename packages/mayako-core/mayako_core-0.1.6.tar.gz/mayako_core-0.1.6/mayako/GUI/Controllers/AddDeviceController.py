from tkinter import messagebox
import tkinter as tk
import threading

from ..Views.MainView import MainView
from ..Views.AddDeviceView import AddDeviceView
from ...Network.NetworkInterface import NetworkProtocols
from ...Service.SerialScanner import scan_serial_ports
from ...Service.ArduinoUploader import ArduinoUploader
from ...MayakoData import MayakoData
from ...Devices.MicroController import MicroControllerCapabilities
from ...Config import CNETWORK
from ...Client import Client
from ...Models.WiFiProfile import WiFiProfile
from ...Models.BLEInfo import BLEInfo

class AddDeviceController:
    """
    this class adds a new mayako-node device to the mayako-core project.
    """
    main_view: MainView
    add_device_frame: AddDeviceView
    uploading: bool

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.main_view = main_view
        self.model = model
        self.client = client
        self.add_device_frame = self.main_view.frame_classes["add_device"]#type: ignore
        self._bind()
        self._model_subscribe()
        self.uploading = False

        self._load_wifi_profiles_into_list()
        self._load_serial_ports_into_list()

    def _load_wifi_profiles_into_list(self) -> None:
        self.add_device_frame.wifi_profile_listbox.delete(0, tk.END)

        for key, wifi_profile in enumerate(self.model.get_wifi_profiles()):
            self.add_device_frame.wifi_profile_listbox.insert(key, wifi_profile.format_string())

    def _load_serial_ports_into_list(self) -> None:
        self.add_device_frame.serial_port_listbox.delete(0, tk.END)

        for key, serial_port in enumerate(self.model.get_serial_ports()):
            self.add_device_frame.serial_port_listbox.insert(key, serial_port.format_string())
            
    def _bind(self) -> None:
        self.add_device_frame.return_btn.config(command=self._return_to_main)
        self.add_device_frame.ble_check.config(command=self._selected_ble)
        self.add_device_frame.wifi_check.config(command=self._selected_wifi)
        self.add_device_frame.flash_device_btn.config(command=self._flash_device)
        self.add_device_frame.wifi_var.trace_add("write", callback=self._toggle_wifi_profiles)
        self.add_device_frame.serial_devices_update_btn.config(command=self._udpate_serial_devices)

    def _model_subscribe(self) -> None:
        self.model.subscribe("wifi_profiles_update", self._update_wifi_profiles)
        self.model.subscribe("serial_ports_update", self._update_serial_ports)

    def _update_wifi_profiles(self, *_) -> None:
        self._load_wifi_profiles_into_list()

    def _update_serial_ports(self, *_) -> None:
        self._load_serial_ports_into_list()

    def _return_to_main(self) -> None:
        self.main_view.switch("home")
        self.add_device_frame.ble_var.set(False)
        self.add_device_frame.wifi_var.set(False)
        self.add_device_frame.identity_entry.delete(0, tk.END)
        self.add_device_frame.status_label.config(text=self.add_device_frame.status_text[0][0])
        self.add_device_frame.status_label.config(fg=self.add_device_frame.status_text[0][1])
        self.uploading = False
        self.serial_ports = []
        self.add_device_frame.serial_port_listbox.delete(0, tk.END)

    def _selected_ble(self) -> None:
        selected_ble = self.add_device_frame.ble_var.get()
        if selected_ble:
            self.add_device_frame.wifi_var.set(False)
    
    def _selected_wifi(self) -> None:
        selected_wifi = self.add_device_frame.wifi_var.get()
        if selected_wifi:
            self.add_device_frame.ble_var.set(False)

    def _toggle_wifi_profiles(self, *_) -> None:
        selected_menu = self.add_device_frame.wifi_var.get()
        if selected_menu:
            self.add_device_frame.wifi_profile_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
            self.add_device_frame.wifi_profile_scrollbar.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="nes")
        else:
            self.add_device_frame.wifi_profile_listbox.grid_remove()
            self.add_device_frame.wifi_profile_scrollbar.grid_remove()

    def _udpate_serial_devices(self) -> None:
        #first clear the list to avoid doubles
        self.add_device_frame.serial_port_listbox.delete(0, tk.END)
        
        #scan for serial ports with arduino description
        self.model.add_serial_port(scan_serial_ports(CNETWORK.SERIAL_ARDUINO_WORDS))
        
        self._load_serial_ports_into_list()

    def _flash_device(self) -> None:
        #prevent uploading multiple times
        if self.uploading: return

        #wireless mode
        wireless_mode = None
        if self.add_device_frame.ble_var.get():
            wireless_mode = NetworkProtocols.BLE

        elif self.add_device_frame.wifi_var.get():
            wireless_mode = NetworkProtocols.WIFI

        else:
            messagebox.showerror(title="Error", message="choose BLE or WiFi")
            return
        
        #wifi profile
        wifi_profile: WiFiProfile = None
        if self.add_device_frame.wifi_var.get():
            wifi_profile_key = self.add_device_frame.wifi_profile_listbox.curselection()

            if not wifi_profile_key:
                messagebox.showerror(title="Error", message="choose a wifi profile")
                return
            
            wifi_profile = self.model.get_wifi_profiles()[wifi_profile_key[0]]

            if not wifi_profile:
                messagebox.showerror(title="Error", message="wifi profile not found")
                return
        
        identity = self.add_device_frame.identity_entry.get()
        if len(identity) != 4:
            messagebox.showerror(title="Error", message="identity must be 4 characters long")
            return
        
        if not identity.isascii():
            messagebox.showerror(title="Error", message="identity must be of type ascii")
            return
        
        if self.model.get_microcontroller_capa_by_identity(identity=identity):
            messagebox.showerror(title="Error", message="a microcontroller with this identity is already in use. please use another identity.")
            return
        
        selected_port_key = self.add_device_frame.serial_port_listbox.curselection()
        if not selected_port_key:
            messagebox.showerror(title="Error", message="select a serial port for upload")
            return

        selected_serial_port = self.model.get_serial_ports()[selected_port_key[0]].port

        #disable flash device button
        self.uploading = True

        #show status in status label - progress
        self.show_progress_status()
        
        #upload device
        uploader = None

        user = self.model.get_this_user()

        #TODO: add to thread?
        if wireless_mode == NetworkProtocols.BLE:
            uploader = ArduinoUploader(user.arduino_folder, identity=identity, serial_port=selected_serial_port, wireless_mode=NetworkProtocols.BLE)
        elif wireless_mode == NetworkProtocols.WIFI:
            uploader = ArduinoUploader(user.arduino_folder, identity=identity, serial_port=selected_serial_port, wireless_mode=NetworkProtocols.WIFI, wifi_profile=wifi_profile)
        else:
            messagebox.showerror(title="Error", message="now upload solution for your settings")
            self.uploading = False
            return
        
        if uploader.check_prerequisits():
            success = uploader.upload()
            if success:
                self.show_success_status()

                if wifi_profile is not None:
                    wifi_key = wifi_profile.wifi_key
                else:
                    wifi_key = None

                new_microcontroller = MicroControllerCapabilities(identity=identity, serial_port=selected_serial_port, protocol=wireless_mode, wifi_key=wifi_key)
                
                self.model.add_microcontroller_capa([new_microcontroller])

                t = threading.Thread(target=self.client._scan_ble_address(mc_identity=new_microcontroller.identity))
                t.start()

            else:
                self.show_error_status()

                messagebox.showerror(title="Error", message="there was an error while uploading")

        else:
            self.show_error_status()
            
            messagebox.showerror(title="Error", message="there was a mistake with the prerequisits for the uploader")
      
        self.uploading = False

    def show_progress_status(self):
        self.add_device_frame.status_label.config(fg=self.add_device_frame.status_text[3][1])
        self.add_device_frame.status_label.config(text=self.add_device_frame.status_text[3][0])
        self.add_device_frame.status_label.update()

    def show_error_status(self):
        self.add_device_frame.status_label.config(text=self.add_device_frame.status_text[1][0])
        self.add_device_frame.status_label.config(fg=self.add_device_frame.status_text[1][1])

    def show_success_status(self):
        self.add_device_frame.status_label.config(text=self.add_device_frame.status_text[2][0])
        self.add_device_frame.status_label.config(fg=self.add_device_frame.status_text[2][1])

    