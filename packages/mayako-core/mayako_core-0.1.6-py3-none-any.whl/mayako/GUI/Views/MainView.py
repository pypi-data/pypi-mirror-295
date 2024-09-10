from typing import Dict
import tkinter as tk
from tkinter import Frame
from .DownloadArduinoView import DownloadArduinoView
from .AddDeviceView import AddDeviceView
from .AddWiFiProfileView import AddWiFiProfileView
from .EditWiFiProfileView import EditWiFiProfileView
from .DeviceDetailsView import DeviceDetailsView
from .HomeView import HomeView
from .Root import Root

class MainView():

    frame_classes: Dict[str, Root]

    def __init__(self) -> None:
        self.root = Root()
        self.root.bind("<Control-w>", self.stop_mainloop)
        self.frame_classes = {
            "home": HomeView(self.root),
            "edit_wifi": EditWiFiProfileView(self.root),
            "add_wifi": AddWiFiProfileView(self.root),
            "add_device": AddDeviceView(self.root),
            "device_details": DeviceDetailsView(self.root),
            "download": DownloadArduinoView(self.root)
        }
        self.current_frame: Root = None

    def switch(self, name: str) -> None:
        new_frame = self.frame_classes[name]
        if self.current_frame is not None:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def start_mainloop(self) -> None:
        self.root.mainloop()

    def stop_mainloop(self, *_) -> None:
        self.root.destroy()