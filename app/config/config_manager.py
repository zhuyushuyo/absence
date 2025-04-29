import json
import os
from PyQt6.QtWidgets import QMessageBox

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        default_config = {"version": "1.1.0", "developer": "xAI Team"}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                QMessageBox.warning(None, "Config Error", f"Failed to load config: {str(e)}. Using default.")
                return default_config
        else:
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
            except Exception as e:
                QMessageBox.warning(None, "Config Error", f"Failed to create config: {str(e)}")
                return default_config

    def get_version(self):
        return self.config.get("version", "1.1.0")

    def get_developer(self):
        return self.config.get("developer", "xAI Team")