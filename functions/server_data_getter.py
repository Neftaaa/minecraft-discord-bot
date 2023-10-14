import requests


def get_minecraft_server_data(address: str) -> dict:
    server_data_request = requests.get(f"https://api.mcsrvstat.us/3/{address}")
    return server_data_request.json()
