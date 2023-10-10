import requests


def get_minecraft_server_info(address: str) -> (dict, str | None):
    server_info_request = requests.get(f"https://api.mcsrvstat.us/3/{address}")
    server_info = server_info_request.json()

    if server_info["online"]:
        icon_url = f"https://api.mcsrvstat.us/icon/{address}"
        return server_info, icon_url
    else:
        return server_info, None
