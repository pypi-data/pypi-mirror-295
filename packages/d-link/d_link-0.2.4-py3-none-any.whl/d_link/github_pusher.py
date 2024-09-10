import subprocess
import json
import os
from d_link.settings_manager import SettingsManager

class GitHubPusher:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.repo_url, self.auth_token = self.settings_manager.get_repository()
        self.repo_path = os.getenv('GITHUB_REPO_PATH', '/path/to/your/github-pages/repo')

        if not self.repo_url or not self.auth_token:
            raise ValueError("Repository URL or Auth Token is missing. Run 'set_repository' to configure.")
        if not self.repo_path:
            raise ValueError("Repository path is missing. Set the GITHUB_REPO_PATH environment variable.")

        # Configure Git with the access token
        self._configure_git()

    def _configure_git(self):
        try:
            # Ensure Git is configured with the correct token for the repository
            subprocess.run(["git", "config", "--global", "user.name", "GitHubPusher"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "githubpusher@example.com"], check=True)
            # Set the remote URL with the access token
            remote_url = self.repo_url.replace("https://", f"https://{self.auth_token}@")
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while configuring Git: {e}")

    def push_to_github(self, data, commit_message="Update data from Python script"):
        try:
            # Change directory to the local GitHub Pages repository
            os.chdir(self.repo_path)

            # Save data to JSON file
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)

            # Perform Git operations
            subprocess.run(["git", "add", "data.json"], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)

            print("Data pushed to GitHub successfully!")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while pushing to GitHub: {e}")
