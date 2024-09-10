from tkinter import Frame, Label, Button, Entry
import tkinter as tk

class EditWiFiProfileView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        #headline
        self.headline = Label(self, text="Edit WiFi Profile")
        self.headline.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        #return button
        self.return_btn = Button(self, text="Return")
        self.return_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        #wifi key text box and entry
        self.wifi_key_label = Label(self, text="WiFi Identity:")
        self.wifi_key_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.wifi_key_entry = Label(self)
        self.wifi_key_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        #SSID text box and entry
        self.ssid_label = Label(self, text="SSID:")
        self.ssid_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ssid_entry = Entry(self)
        self.ssid_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        #Password text box and entry
        self.password_label = Label(self, text="Password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = Entry(self)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        #Client IP text box and entry
        self.client_ip_label = Label(self, text="Client IP:")
        self.client_ip_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.client_ip_entry = Entry(self)
        self.client_ip_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        #Client Port text box and entry
        self.client_port_label = Label(self, text="Client Port:")
        self.client_port_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.client_port_entry = Entry(self)
        self.client_port_entry.grid(row=5, column=1, padx=10, pady=5, sticky="we")

        #Create WiFi Profile button
        self.edit_wifi_profile_btn = Button(self, text="Edit")
        self.edit_wifi_profile_btn.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        #label for success, fail, inprogress, idle
        self.status_text = [("", "black"), ("Fail", "red"), ("Success", "green"), ("In Progress", "black")]
        i = 0
        self.status_label = Label(self, text=self.status_text[i][0], fg=self.status_text[i][1])
        self.status_label.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add New WiFi Profile")
    root.geometry("400x620")
    add_wifi_profile_view = EditWiFiProfileView(root)
    add_wifi_profile_view.pack(fill="both", expand=True)
    root.mainloop()
