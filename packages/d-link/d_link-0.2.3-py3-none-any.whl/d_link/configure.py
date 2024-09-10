# d_link/configure.py
from d_link.settings_manager import SettingsManager

def configure():
    """Script to configure d_link settings."""
    settings_manager = SettingsManager()
    settings_manager.display_settings()
    settings_manager.set_repository()
    print("Configuration complete. Your settings have been saved to environment variables.")

if __name__ == "__main__":
    configure()
