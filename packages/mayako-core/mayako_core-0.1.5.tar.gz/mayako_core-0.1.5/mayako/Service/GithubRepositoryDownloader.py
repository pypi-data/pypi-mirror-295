import os
import requests
from requests import Response
from typing import List, Tuple, Optional, Dict


class GithubRepositoryDownloader:
    """
    this class downloads specific folders and files from github repositories,
    stores them in the desired location on the local machine, and returns a status on the requested files.
    """

    def __init__(self, repository_url: str, destination_path: str, github_token: str) -> None:
        """
        initializes the downloader with the github repository URL and the destination path.

        Args
            repository_url (str):
                the url of a public github repository
                Example: https://github.com/vairasza/m5test
            destination_path (str);
                the destination folder in relation to the current working directory
                Example: arduino
        """
        self.repository_url = repository_url
        self.destination_path = destination_path
        self.github_token = github_token
        repo_info = self.repository_url.rstrip('/').split("/")
        self.owner = repo_info[-2]
        self.repository_name = repo_info[-1]

        self.api_url = f"https://api.github.com/repos/{self.owner}/{self.repository_name}/contents/"
        self.download_status: List[Tuple[str, str]] = []

        self._create_folder(self.destination_path)

    def _create_folder(self, folder_path: str) -> None:
        """
        creates the destination folder if it does not yet exist.
        
        Args
            folder_path (str):
                Example: lib
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _download_content(self, url: str) -> Optional[Response]:
        """
        downloads the content from the gtihub repository and returns the response object.
        The response can be a list (folder item) or a dict (file).
        The reponse object must be converted to json with response.json(). it results in a list of dictionaries or a dictionary. list ^= folder; dict ^= file

        Args
            path
                url for github content api

        Return
            Response or None:
                a request response object or none is the result of this function
        """

        if self.github_token:
            headers = { 'Authorization': f"Bearer {self.github_token}" }
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response
        else:
            return None

    def _record_status(self, path: str, success: bool) -> None:
        """
        records the download status of a file or folder.
        
        Args
            path (str):
                Example: lib/test/Accelerometer.cpp 
            success (bool):
                if the content could be downloaded successfully or not
        """
        status = "success" if success else "fail"
        self.download_status.append((path, status))

    def _download_folder(self, dest_folder_path: str, folder_items: List[Dict]) -> None:
        """
        downloads the contents of a folder recursivly.

        Args
            dest_path (str):
                Example lib
            folder_items (List[Dict]):
                a list of dictionaries which describe the content of a github repo file. see source in top comment.
        """
        full_dest_path = os.path.join(self.destination_path, dest_folder_path)
        self._create_folder(full_dest_path)

        for folder_item in folder_items:
            item_path = folder_item['path']
            if folder_item['type'] == 'file':
                self._download_file(item_path, folder_item)

            elif folder_item['type'] == 'dir':
                url = self.api_url + item_path
                response = self._download_content(url)
                if not response:
                    self._record_status(item_path, False)
                    continue

                subfolder_info = response.json()
                self._download_folder(item_path, subfolder_info)

    def _download_file(self, dest_file_path: str, file_info: Dict) -> None:
        """
        downloads a single file and maintains the repositorys directory structure in the destination.

        Args
            dest_path (str):
                Example lib
            file_info (Dict):
                a dictionary which describe the content of a github repo file. see source in top comment.
        """
        file_url = file_info.get('download_url')

        if not file_url:
            self._record_status(dest_file_path, False)
            return

        #check if structure exists
        file_destination_dir = os.path.dirname(os.path.join(self.destination_path, dest_file_path))
        self._create_folder(file_destination_dir)

        try:
            file_response = self._download_content(file_url)
            file_destination = os.path.join(self.destination_path, dest_file_path)

            with open(file_destination, 'wb') as file:
                file.write(file_response.content)

            self._record_status(dest_file_path, True)

        except Exception as e:
            self._record_status(dest_file_path, False)

    def download(self, paths: List[str]) -> List[Tuple[str, str]]:
        """
        downloads only the specified files and folders
        
        Args
            paths (List[str]):
                Example: ["platformio.ini", "lib", "src"]
        
        Return
            List[Tuple[str, str]]
                Example  [(Success:,lib/README),(Fail:,lib/test/Accelerometer.cpp)]
        """
        for path in paths:
            url = self.api_url + path
            response = self._download_content(url)
            if not response:
                self._record_status(path, False)
                continue

            item_info = response.json()

            # ceck if item_info is a list => download_folder
            if isinstance(item_info, list):
                self._download_folder(path, item_info)
            # otherwise, it's a file
            else:
                self._download_file(path, item_info)

        return self.download_status

if __name__ == "__main__":
    #example usage
    repo_url = "https://github.com/vairasza/m5test"
    destination = "arduino"
    selected_paths = ["platformio.ini", "lib", "src"]
    g = GithubRepositoryDownloader(repository_url=repo_url, destination_path=destination)
    results = g.download(selected_paths)

    for path, status in results:
        print(f"{status}: {path}")
