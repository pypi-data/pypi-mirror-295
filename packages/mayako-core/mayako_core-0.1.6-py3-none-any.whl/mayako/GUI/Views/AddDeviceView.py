from tkinter import Frame, Label, Button, Listbox, Scrollbar, Entry, Checkbutton, BooleanVar
import tkinter as tk

class AddDeviceView(Frame):
    def __init__(self, *args, **kwargs):
        """
        Sources:
            https://stackoverflow.com/a/26366001
        """
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        #headline
        self.headline = Label(self, text="Add New Device")
        self.headline.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        #return button
        self.return_btn = Button(self, text="Return")
        self.return_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        #checkboxes
        self.ble_var = BooleanVar()
        self.wifi_var = BooleanVar()
        self.ble_check = Checkbutton(self, text="BLE", variable=self.ble_var, onvalue=True, offvalue=False)
        self.ble_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.wifi_check = Checkbutton(self, text="WiFi", variable=self.wifi_var, onvalue=True, offvalue=False)
        self.wifi_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        #list of wifi profiles
        self.wifi_profile_listbox = Listbox(self, selectmode="single", exportselection=False)
        #self.wifi_profile_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.wifi_profile_scrollbar = Scrollbar(self, orient="vertical", command=self.wifi_profile_listbox.yview)
        #self.wifi_profile_scrollbar.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="nes")
        self.wifi_profile_listbox.config(yscrollcommand=self.wifi_profile_scrollbar.set)

        #identity text box
        self.identity_label = Label(self, text="Identity: (must be 4 chars long)")
        self.identity_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.identity_entry = Entry(self)
        self.identity_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        #select devices text
        self.select_devices_label = Label(self, text="Select the serial port the device is connected to:")
        self.select_devices_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.serial_devices_update_btn = Button(self, text="Update")
        self.serial_devices_update_btn.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        #listbox for seria port
        self.serial_port_listbox = Listbox(self, selectmode="single", exportselection=False)
        self.serial_port_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.serial_port_scrollbar = Scrollbar(self, orient="vertical", command=self.serial_port_listbox.yview)
        self.serial_port_scrollbar.grid(row=6, column=1, padx=(0, 10), pady=5, sticky="nes")
        self.serial_port_listbox.config(yscrollcommand=self.serial_port_scrollbar.set)

        #flash button
        self.flash_device_btn = Button(self, text="Flash Device")
        self.flash_device_btn.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        #label for success, fail, inprogress, idle
        self.status_text = [("", "black"), ("Fail", "red"), ("Success", "green"), ("In Progress", "black")]
        i = 0
        self.status_label = Label(self, text=self.status_text[i][0], fg=self.status_text[i][1])
        self.status_label.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.info_label = Label(self, text="🛈 flashing the microcontroller might take a while. (approximately  1-2 mins)")
        self.info_label.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        self.wifi_profile_listbox.bind("<FocusIn>", lambda event: self.wifi_profile_listbox.selection_clear(0, tk.END))
        self.serial_port_listbox.bind("<FocusIn>", lambda event: self.serial_port_listbox.selection_clear(0, tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add New Device")
    root.geometry("400x620")
    add_device_view = AddDeviceView(root)
    add_device_view.pack(fill="both", expand=True)
    root.mainloop()
