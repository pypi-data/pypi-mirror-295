from tkinter import Frame, Label, Button, Listbox, Scrollbar, VERTICAL, SINGLE
import tkinter as tk

class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)  # No weight for the scrollbar column

        # Download Arduino Project from Github
        self.get_arduino_btn = Button(self, text="Get Arduino Project")
        self.get_arduino_btn.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="we")

        # Devices Section
        self.devices_label = Label(self, text="Devices")
        self.devices_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.devices_listbox = Listbox(self, selectmode=SINGLE)
        self.devices_listbox.grid(row=2, column=0, columnspan=3, padx=(10, 0), pady=5, sticky="nsew")

        self.devices_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.devices_listbox.yview)
        self.devices_scrollbar.grid(row=2, column=3, padx=(0, 10), pady=5, sticky="ns")
        self.devices_listbox.config(yscrollcommand=self.devices_scrollbar.set)

        self.add_device_btn = Button(self, text="Add")
        self.add_device_btn.grid(row=3, column=0, padx=10, pady=5)

        self.remove_device_btn = Button(self, text="Remove")
        self.remove_device_btn.grid(row=3, column=1, padx=10, pady=5)

        self.device_details_btn = Button(self, text="Details")
        self.device_details_btn.grid(row=3, column=2, padx=10, pady=5)

        # Wi-Fi Profiles Section
        self.wifi_label = Label(self, text="Wi-Fi Profiles")
        self.wifi_label.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.wifi_listbox = Listbox(self, selectmode=SINGLE)
        self.wifi_listbox.grid(row=5, column=0, columnspan=3, padx=(10, 0), pady=5, sticky="nsew")

        self.wifi_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.wifi_listbox.yview)
        self.wifi_scrollbar.grid(row=5, column=3, padx=(0, 10), pady=5, sticky="ns")
        self.wifi_listbox.config(yscrollcommand=self.wifi_scrollbar.set)

        self.add_wifi_btn = Button(self, text="Add")
        self.add_wifi_btn.grid(row=6, column=0, padx=10, pady=5)

        self.remove_wifi_btn = Button(self, text="Remove")
        self.remove_wifi_btn.grid(row=6, column=1, padx=10, pady=5)

        self.wifi_details_btn = Button(self, text="Edit")
        self.wifi_details_btn.grid(row=6, column=2, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add New Device")
    root.geometry("400x620")
    add_device_view = HomeView(root)
    add_device_view.pack(fill="both", expand=True)
    root.mainloop()
