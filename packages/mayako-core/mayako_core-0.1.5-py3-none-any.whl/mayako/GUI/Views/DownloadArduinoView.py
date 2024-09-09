from tkinter import Frame, Label, Button, Entry, Text, Scrollbar, VERTICAL
import tkinter as tk

class DownloadArduinoView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(9, weight=1) 

        #headline
        self.headline = Label(self, text="Download Arduino Project")
        self.headline.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        #return button
        self.return_btn = Button(self, text="Return")
        self.return_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # GitHub Repository Entry
        self.repo_url_label = Label(self, text="Github Repository URL")
        self.repo_url_label.grid(row=1, column=0, padx=10,  sticky="w")
        self.repo_url_entry = Entry(self)
        self.repo_url_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        self.repo_url_entry.insert(0, "https://github.com/vairasza/mayako-node")

        #GitHub Access Token which helps increase the rate limit drastically
        self.gh_token_label = Label(self, text="Github Access Token (optional)")
        self.gh_token_label.grid(row=3, column=0, padx=10,  sticky="w")
        self.gh_token_entry = Entry(self)
        self.gh_token_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        # Destination Entry
        self.destination_label = Label(self, text="Target Folder for the Arduino Project")
        self.destination_label.grid(row=5, column=0, padx=10,  sticky="w")
        self.destination_entry = Entry(self)
        self.destination_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        self.destination_entry.insert(0, "arduino")

        #flash button
        self.download_btn = Button(self, text="Download")
        self.download_btn.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        #label for success, fail, inprogress, idle
        self.status_text = [("", "black"), ("Fail", "red"), ("Success", "green"), ("In Progress", "black")]
        self.status_label = Label(self, text=self.status_text[0][0], fg=self.status_text[0][1])
        self.status_label.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.download_hint = Label(self, text="🛈 After downloading the Arduino Project, check the repository's documentation if you intend to modify the code or want to extend it with additional sensors or actuators. Happy coding!", wraplength=650, justify="left")
        self.download_hint.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        #output for result of download
        self.result_text = Text(self)
        self.result_text.grid(row=9, column=0, columnspan=2, padx=(10, 0), pady=5, sticky="ew")
        self.result_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.result_text.yview)
        self.result_scrollbar.grid(row=9, column=2, padx=(0, 10), pady=5, sticky="nesw")
        self.result_text.config(yscrollcommand=self.result_scrollbar.set)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add New WiFi Profile")
    root.geometry("450x600")
    add_wifi_profile_view = DownloadArduinoView(root)
    add_wifi_profile_view.pack(fill="both", expand=True)
    root.mainloop()
