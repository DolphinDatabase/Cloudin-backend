import json

file_path = "config.json"


def load_json_file():
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_json_file(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
