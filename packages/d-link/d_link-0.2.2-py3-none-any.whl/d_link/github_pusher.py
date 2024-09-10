import subprocess
import json
import os
from settings_manager import SettingsManager

class GitHubPusher:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.repo_url, self.auth_token = self.settings_manager.get_repository()

        if not self.repo_url or not self.auth_token:
            raise ValueError("Repository URL or Auth Token is missing. Run 'set_repository' to configure.")

    def push_to_github(self, data, commit_message="Update data from Python script"):
        try:
            repo_path = "/path/to/your/github-pages/repo"  # Adjust the path to your repo
            os.chdir(repo_path)

            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)

            subprocess.run(["git", "add", "data.json"], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True, env={"GITHUB_TOKEN": self.auth_token})

            print("Data pushed to GitHub successfully!")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
