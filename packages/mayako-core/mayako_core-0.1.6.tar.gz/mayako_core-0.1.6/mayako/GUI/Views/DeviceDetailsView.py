from tkinter import Frame, Label, Button, Text, Scrollbar, VERTICAL
import tkinter as tk

class DeviceDetailsView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1) 

        #headline
        self.headline = Label(self, text="Device Details")
        self.headline.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        #return button
        self.return_btn = Button(self, text="Return")
        self.return_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Identity Label
        self.identity_label = Label(self, text="Identity")
        self.identity_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.identity_text = Label(self)
        self.identity_text.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #protocol used label
        self.protocol_label = Label(self, text="Protocol")
        self.protocol_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.protocol_text = Label(self)
        self.protocol_text.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        #battery
        self.battery_label = Label(self, text="Battery")
        self.battery_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.battery_text = Label(self)
        self.battery_text.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        #capabiltiies
        self.update_capabilities_btn = Button(self, text="Update Capabilities")
        self.update_capabilities_btn.grid(row=4, column=0, padx=10, pady=5)
        #self.update_capabilities_btn.config(state="disabled")#disabled while device not connected

        #Identify
        #self.identify_device_btn = Button(self, text="Identify Device")
        #self.identify_device_btn.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        #text field for capabiltiies
        self.capabilities_text = Text(self)
        self.capabilities_text.grid(row=5, column=0, columnspan=2, padx=(10, 0), pady=5, sticky="nesw")
    
        self.capabiltiies_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.capabilities_text.yview)
        self.capabiltiies_scrollbar.grid(row=5, column=2, padx=(0, 10), pady=5, sticky="nes")
        self.capabilities_text.config(yscrollcommand=self.capabiltiies_scrollbar.set)

        #label for success, fail, inprogress, idle
        self.status_text = [("", "black"), ("Fail", "red"), ("Success", "green"), ("In Progress", "black")]
        i = 0
        self.status_label = Label(self, text=self.status_text[i][0], fg=self.status_text[i][1])
        self.status_label.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add New WiFi Profile")
    root.geometry("450x600")
    add_wifi_profile_view = DeviceDetailsView(root)
    add_wifi_profile_view.pack(fill="both", expand=True)
    root.mainloop()
