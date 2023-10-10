import json


def get_data_from_json(file_path: str) -> list:
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def update_json_data(data, file_path: str):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


def get_remote_minecraft_address(guild_id: int, server_address: str, json_path: str) -> str | None:
    if server_address == "" or server_address is None:
        data = get_data_from_json(json_path)

        for data_objet in data:
            if guild_id == data_objet["guild_id"]:
                return data_objet["default_address"]

        return None

    return server_address
