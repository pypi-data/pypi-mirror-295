from .data_extractor import DataExtractor
from .github_pusher import GitHubPusher
from d_link.settings_manager import SettingsManager

class DataToGitHub:
    def __init__(self, script_path):
        self.script_path = script_path
        self.data_extractor = DataExtractor(script_path)
        self.github_pusher = GitHubPusher()

    def configure_repository(self):
        self.settings_manager = SettingsManager()
        self.settings_manager.set_repository()

    def display_settings(self):
        self.settings_manager = SettingsManager()
        self.settings_manager.display_settings()

    def push_data(self):
        data = self.data_extractor.extract_data()
        self.github_pusher.push_to_github(data, 'Update data from Python script')
