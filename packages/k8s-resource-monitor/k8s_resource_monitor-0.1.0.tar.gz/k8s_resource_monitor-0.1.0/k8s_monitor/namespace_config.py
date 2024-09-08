import json
import os

NAMESPACE_FILE = "namespaces.json"

def load_namespaces():
    """
    Load the list of namespaces to monitor from the namespaces.json file.
    """
    if os.path.exists(NAMESPACE_FILE):
        with open(NAMESPACE_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_namespaces(namespaces):
    """
    Save the list of namespaces to the namespaces.json file.
    """
    with open(NAMESPACE_FILE, 'w') as file:
        json.dump(namespaces, file, indent=4)

def view_namespaces():
    """
    Display the current namespaces being monitored.
    """
    namespaces = load_namespaces()
    if 'namespaces' in namespaces:
        print("Monitoring the following namespaces:")
        for ns in namespaces['namespaces']:
            print(f"- {ns}")
    else:
        print("No namespaces configured for monitoring.")

def reset_namespaces():
    """
    Reset the namespace list by clearing the namespaces.json file.
    """
    if os.path.exists(NAMESPACE_FILE):
        os.remove(NAMESPACE_FILE)
        print("Namespaces reset successfully.")
    else:
        print("No namespace file found to reset.")
