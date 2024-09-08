import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """
    Load configuration from the config.json file.
    If it doesn't exist, return an empty dictionary.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_config(config):
    """
    Save configuration to the config.json file.
    """
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def view_config():
    """
    Display the current configuration.
    """
    config = load_config()
    if config:
        for key, value in config.items():
            print(f"{key}: {value}")
    else:
        print("No configuration found.")

def reset_config():
    """
    Reset the configuration by deleting the config.json file.
    """
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("Configuration reset successfully.")
    else:
        print("No configuration file found to reset.")
