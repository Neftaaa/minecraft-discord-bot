from os import path, listdir


def get_bot_token() -> str:
    if path.exists("token.txt"):
        with open("token.txt", "r") as token_file:
            return token_file.read()

    open("token.txt", "w+")
    raise Exception("Can't find token file, created a new one named: 'token.txt'. Please write the bot token in this file.")


def get_supported_languages() -> (list, str):
    supported_languages_list = []
    languages_dir = 'languages'
    for filename in listdir(languages_dir):
        normalized_filename = filename.split(".")[0]
        supported_languages_list.append(normalized_filename)

    supported_languages_str = ""
    for language in supported_languages_list:
        supported_languages_str += language + ", "
    supported_languages_str = supported_languages_str[:-2]

    return supported_languages_list, supported_languages_str
