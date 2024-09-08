import json
import os

AUTOSCALING_POLICY_FILE = "autoscaling_policy.json"

def load_autoscaling_policy():
    """
    Load the auto-scaling policy from the autoscaling_policy.json file.
    """
    if os.path.exists(AUTOSCALING_POLICY_FILE):
        with open(AUTOSCALING_POLICY_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_autoscaling_policy(policy):
    """
    Save the auto-scaling policy to the autoscaling_policy.json file.
    """
    with open(AUTOSCALING_POLICY_FILE, 'w') as file:
        json.dump(policy, file, indent=4)

def view_autoscaling_policy():
    """
    Display the current auto-scaling policy.
    """
    policy = load_autoscaling_policy()
    if policy:
        for key, value in policy.items():
            print(f"{key}: {value}")
    else:
        print("No auto-scaling policy found.")

def reset_autoscaling_policy():
    """
    Reset the auto-scaling policy by deleting the autoscaling_policy.json file.
    """
    if os.path.exists(AUTOSCALING_POLICY_FILE):
        os.remove(AUTOSCALING_POLICY_FILE)
        print("Auto-scaling policy reset successfully.")
    else:
        print("No auto-scaling policy file found to reset.")
