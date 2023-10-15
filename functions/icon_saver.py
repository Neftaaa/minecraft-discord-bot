import base64


def save_icon(file_path: str, icon: str):
    head, data = icon.split(',', 1)
    plain_data = base64.b64decode(data)

    with open(file_path, 'wb') as f:
        f.write(plain_data)
