import tkinter as tk
from tkinter import messagebox

from ...Models.User import User
from ..Views.MainView import MainView
from ..Views.DownloadArduinoView import DownloadArduinoView
from ...Service.GithubRepositoryDownloader import GithubRepositoryDownloader
from ...MayakoData import MayakoData
from ...Config import CNETWORK
from ...Service.MacAdress import get_macaddress
from ...Utils.Logger import LoggerType, LoggerInstance
from ...Client import Client

class DownloadArduinoController:
    """
    this class downloads parts of a github repository into a selected folder.

    this is a controller class for the tkinter GUI.
    """
    logger: LoggerType
    main_view: MainView
    download_frame: DownloadArduinoView
    uploading: bool

    def __init__(self, main_view: MainView, model: MayakoData, client: Client) -> None:
        self.logger = LoggerInstance.get()
        self.main_view = main_view
        self.model = model
        self.client = client
        self.download_frame = self.main_view.frame_classes["download"]#type: ignore
        self._bind()
        self.uploading = False

    def _bind(self) -> None:
        self.download_frame.return_btn.config(command=self._return_to_main)
        self.download_frame.download_btn.config(command=self._dowload_repository)

    def _return_to_main(self) -> None:
        self.main_view.switch("home")
        self.download_frame.repo_url_entry.delete(0, tk.END)
        self.download_frame.destination_entry.delete(0, tk.END)
        self.download_frame.gh_token_entry.delete(0, tk.END)
        self.uploading = False
        self.download_frame.status_label.config(fg=self.download_frame.status_text[0][1])
        self.download_frame.status_label.config(text=self.download_frame.status_text[0][0])
        self.download_frame.result_text.delete("1.0", tk.END)

    def _dowload_repository(self) -> None:
        if self.uploading: return

        gh_url = self.download_frame.repo_url_entry.get()
        token = self.download_frame.gh_token_entry.get()
        dest = self.download_frame.destination_entry.get()

        if gh_url == "":
            messagebox.showerror(title="Error", message="Github Repostory URL must be a valid URL to a GitHub repository")

            return
        
        if dest == "":
            messagebox.showerror(title="Error", message="destination must be a valid folder")

            return

        self.uploading = True

        #show status in status label - progress
        self.show_progress_status()

        try:
            downloader = GithubRepositoryDownloader(repository_url=gh_url, destination_path=dest, github_token=token)
            results = downloader.download(CNETWORK.SELECTED_PATHS)

            for path, status in results:
                self.download_frame.result_text.insert(tk.END, f"{status}: {path}\n")

            user_mac_address = get_macaddress()
            user = User(user_mac_address=user_mac_address, arduino_folder=dest)
            self.model.add_user(user)

            self.show_success_status()
        
        except Exception as e:
            #show error status
            self.logger.error(e)
            self.show_error_status()

            messagebox.showerror(title="Error", message="there was an error while uploading")
        
        self.uploading = False

    def show_error_status(self):
        self.download_frame.status_label.config(text=self.download_frame.status_text[1][0])
        self.download_frame.status_label.config(fg=self.download_frame.status_text[1][1])

    def show_success_status(self):
        self.download_frame.status_label.config(text=self.download_frame.status_text[2][0])
        self.download_frame.status_label.config(fg=self.download_frame.status_text[2][1])

    def show_progress_status(self):
        self.download_frame.status_label.config(fg=self.download_frame.status_text[3][1])
        self.download_frame.status_label.config(text=self.download_frame.status_text[3][0])
        self.download_frame.status_label.update()