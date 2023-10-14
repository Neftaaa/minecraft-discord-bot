import requests


def get_minecraft_server_info(address: str) -> dict:
    server_info_request = requests.get(f"https://api.mcsrvstat.us/3/{address}")
    return server_info_request.json()
