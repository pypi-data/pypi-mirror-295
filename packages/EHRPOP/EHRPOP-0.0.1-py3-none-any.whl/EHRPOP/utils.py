import json
import os

def load_json_data():
    # Define the path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), 'all_codes.json')

    # Load the JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data
