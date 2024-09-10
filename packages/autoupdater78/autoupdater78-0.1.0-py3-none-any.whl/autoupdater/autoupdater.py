import os
import hashlib
import json
import requests
from urllib.parse import urljoin
import sys
from collections import OrderedDict

class AutoUpdater:
    def __init__(self, local_directory, remote_base_url):
        self.local_directory = local_directory
        self.remote_base_url = remote_base_url
        self.remote_md5_url = urljoin(remote_base_url, "md5.json")

    def calculate_file_md5(self, filepath):
        """Calculate MD5 hash of a file"""
        md5_hash = hashlib.md5()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def get_file_list_with_md5(self, directory):
        """Get a list of all files in the directory with their MD5 values, excluding md5.json"""
        file_list = OrderedDict()
        for root, _, files in os.walk(directory):
            for file in sorted(files):
                if file != "md5.json":
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, directory)
                    file_list[relative_path] = self.calculate_file_md5(filepath)
        return file_list

    def save_md5_json(self, output_file="md5.json"):
        """Generate and save JSON file containing file MD5 values"""
        md5_list = self.get_file_list_with_md5(self.local_directory)
        output_path = os.path.join(self.local_directory, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(md5_list, f, ensure_ascii=False, indent=2, sort_keys=True)
        return output_path

    def download_file(self, url, filepath):
        """Download file to specified path"""
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(response.content)

    def update_files(self):
        """Update local files based on remote MD5 file list"""
        try:
            response = requests.get(self.remote_md5_url)
            response.raise_for_status()
            remote_md5_list = response.json()
            
            local_md5_list = self.get_file_list_with_md5(self.local_directory)
            
            updated_files = []
            for filepath, remote_md5 in remote_md5_list.items():
                if filepath != "md5.json":
                    local_filepath = os.path.join(self.local_directory, filepath)
                    if filepath not in local_md5_list or local_md5_list[filepath] != remote_md5:
                        print(f"Updating file: {filepath}")
                        remote_file_url = urljoin(self.remote_base_url, filepath)
                        self.download_file(remote_file_url, local_filepath)
                        updated_files.append(filepath)
            
            return json.dumps({
                "status": "success",
                "updated_files": updated_files
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            }, ensure_ascii=False)

    def initialize_local_directory(self):
        """Initialize local directory"""
        try:
            os.makedirs(self.local_directory, exist_ok=True)
            
            local_md5_file = self.save_md5_json()
            
            print(f"Generated md5.json file: {local_md5_file}")
            
            return json.dumps({
                "status": "success",
                "message": f"Local directory '{self.local_directory}' has been initialized",
                "md5_file": local_md5_file,
                "md5_content": self.get_file_list_with_md5(self.local_directory)
            }, ensure_ascii=False)
        except Exception as e:
            print(f"Error initializing local directory: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": str(e)
            }, ensure_ascii=False)

def update_files(local_directory, remote_base_url):
    updater = AutoUpdater(local_directory, remote_base_url)
    return updater.update_files()

def initialize_directory(local_directory, remote_base_url):
    try:
        print(f"Initializing directory: {local_directory}")
        print(f"Remote base URL: {remote_base_url}")
        updater = AutoUpdater(local_directory, remote_base_url)
        result = updater.initialize_local_directory()
        print(f"Initialization result: {result}")
        return result
    except Exception as e:
        print(f"Exception during initialization: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python autoupdater.py initialize_directory <local_directory> <remote_base_url>")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "initialize_directory":
        result = initialize_directory(sys.argv[2], sys.argv[3])
        print(result)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)