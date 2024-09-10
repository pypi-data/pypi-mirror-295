import json
import os

class SettingsManager:
    CONFIG_FILE = "config.json"

    def __init__(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'repository_url': '',
                'auth_token': ''
            }

    def set_repository(self):
        repo_url = input("Enter the GitHub repository URL: ")
        self.config['repository_url'] = repo_url

        auth_token = input("Enter your GitHub personal access token: ")
        self.config['auth_token'] = auth_token

        self._save_config()
        print(f"Settings updated successfully. Repository URL: {repo_url}")

    def _save_config(self):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_repository(self):
        return self.config.get('repository_url', ''), self.config.get('auth_token', '')

    def display_settings(self):
        print("Current Settings:")
        print(f"Repository URL: {self.config['repository_url']}")
        print(f"Auth Token: {self.config['auth_token'][:4]}**** (hidden for security)")
