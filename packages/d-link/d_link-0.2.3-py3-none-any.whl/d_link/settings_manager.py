# d_link/settings_manager.py
import os

class SettingsManager:
    def __init__(self):
        """Initialize SettingsManager by loading the existing configuration from environment variables."""
        self.repository_url = os.getenv('GITHUB_REPO_URL', '')
        self.auth_token = os.getenv('GITHUB_AUTH_TOKEN', '')

    def set_repository(self):
        """Prompt user to set GitHub repository URL and access token and save them to environment variables."""
        print("Let's set up your GitHub repository and access token.")

        repo_url = self._prompt_input("Enter the GitHub repository URL (e.g., your-username/your-repo): ")
        if not repo_url:
            print("Repository URL cannot be empty.")
            return
        
        auth_token = self._prompt_input("Enter your GitHub personal access token: ")
        if not auth_token:
            print("Access token cannot be empty.")
            return

        os.environ['GITHUB_REPO_URL'] = repo_url
        os.environ['GITHUB_AUTH_TOKEN'] = auth_token
        print(f"Settings updated successfully. Repository URL: {repo_url}")

    def _prompt_input(self, prompt):
        """Helper method for prompting user input."""
        return input(prompt).strip()

    def display_settings(self):
        """Display current configuration settings with sensitive information hidden."""
        print("Current Settings:")
        repo_url = self.repository_url if self.repository_url else 'Not set'
        auth_token = self.auth_token if self.auth_token else 'Not set'
        print(f"Repository URL: {repo_url}")
        print(f"Auth Token: {auth_token[:4]}**** (hidden for security)")

    def get_repository(self):
        """Retrieve the repository URL and token from environment variables."""
        return os.getenv('GITHUB_REPO_URL', ''), os.getenv('GITHUB_AUTH_TOKEN', '')
