import discord
from datetime import datetime
from src.functions.interactions_data_processors import get_language_data


def convert_server_data_dict(server_data: dict) -> dict:
    motd = server_data["motd"]
    clean_motd = motd["clean"]
    if len(clean_motd) == 1:
        usable_motd = clean_motd[0]
    else:
        usable_motd = f"{clean_motd[0]}\n{clean_motd[1]}"

    players_info = server_data["players"]
    online_player_count = players_info["online"]
    max_player_count = players_info["max"]

    version = server_data["version"]
    return {"final_motd": usable_motd, "online_player_count": online_player_count,
            "max_player_count": max_player_count, "version": version}


def build_help_embed(supported_languages: str, lang: str) -> discord.embeds.Embed:
    language_data = get_language_data(lang)

    help_embed = discord.Embed(title="Help", color=discord.Color.green())
    help_embed.add_field(name=language_data["help_embed_bot_info"], value=f"```{language_data['help_embed_bot_info_value']}```", inline=False)
    help_embed.add_field(name="</help:1161352090501775471>", value=f"```{language_data['help_embed_/help_value']}```", inline=False)
    help_embed.add_field(name="</server-info:1162832201105293484> `address`", value=f"```{language_data['help_embed_/server-info_value']}```", inline=False)
    help_embed.add_field(name="</set-default:1162832201105293482>  `default_address`", value=f"```{language_data['help_embed_/set-default_value']}```", inline=False)
    help_embed.add_field(name="</current-default:1162832201105293483>", value=f"```{language_data['help_embed_/current_default_value']}```")
    help_embed.add_field(name="</language:1163048440410939452> `lang`", value=f"```{language_data['help_embed_/language_value']}{supported_languages}```", inline=False)
    return help_embed


def build_online_server_embed(server_data: dict, address, icon_path: str, lang: str) -> (discord.embeds.Embed, discord.File):
    language_data = get_language_data(lang)

    usable_server_data = convert_server_data_dict(server_data)
    server_icon = discord.File(icon_path, filename="default_icon.png")

    server_data_embed = discord.Embed(title=language_data["online_server_embed_title"], color=discord.Color.green())

    server_data_embed.set_author(name=address, icon_url="attachment://default_icon.png")
    server_data_embed.set_thumbnail(url="attachment://default_icon.png")

    server_data_embed.add_field(name="MOTD:", value=f"```{usable_server_data['final_motd']}```", inline=False)
    server_data_embed.add_field(name=language_data["online_server_embed_status"], value=f"`{language_data['online_server_embed_online']}`", inline=True)
    server_data_embed.add_field(name=language_data["online_server_embed_players"], value=f"`{usable_server_data['online_player_count']}"
                                                                                         f"/{usable_server_data['max_player_count']}`", inline=True)
    server_data_embed.add_field(name=language_data["online_server_embed_version"], value=f"`{usable_server_data['version']}`", inline=True)

    server_data_embed.timestamp = datetime.now()
    server_data_embed.set_footer(text="\u200B", icon_url="attachment://default_icon.png")
    return server_data_embed, server_icon


def build_unreachable_server_embed(address, lang: str) -> (discord.embeds.Embed, discord.File):
    language_data = get_language_data(lang)

    error_image = discord.File("resources/error.png", filename="error.png")

    server_data_embed = discord.Embed(title=language_data["unreachable_server_embed_title"], color=discord.Color.red())

    server_data_embed.add_field(name="", value=f"`{language_data['unreachable_server_embed_field']}`")

    server_data_embed.set_author(name=address, icon_url="attachment://error.png")
    server_data_embed.set_thumbnail(url="attachment://error.png")

    server_data_embed.timestamp = datetime.now()
    server_data_embed.set_footer()
    return server_data_embed, error_image


def build_default_address_embed(default_address: str, lang: str) -> (discord.embeds.Embed, discord.File):
    language_data = get_language_data(lang)

    valid_image = discord.File("resources/valid.png", filename="valid.png")

    default_address_embed = discord.Embed(title=f"{language_data['default_address_embed_title']}`'{default_address}'`", color=discord.Color.green())
    default_address_embed.set_author(name=default_address, icon_url="attachment://valid.png")
    default_address_embed.set_thumbnail(url="attachment://valid.png")

    default_address_embed.timestamp = datetime.now()
    default_address_embed.set_footer()
    return default_address_embed, valid_image


def build_language_embed(lang: str) -> (discord.embeds.Embed, discord.File):
    language_data = get_language_data(lang)

    valid_image = discord.File("resources/valid.png", filename="valid.png")

    default_address_embed = discord.Embed(title=f"{language_data['language_embed_title']}`'{lang}'`", color=discord.Color.green())
    default_address_embed.set_author(name=lang, icon_url="attachment://valid.png")
    default_address_embed.set_thumbnail(url="attachment://valid.png")

    default_address_embed.timestamp = datetime.now()
    default_address_embed.set_footer()
    return default_address_embed, valid_image


def build_not_assigned_default_address_embed(lang: str) -> discord.embeds.Embed:
    language_data = get_language_data(lang)

    not_assigned_default_address_embed = discord.Embed(title=language_data["default_address_not_assigned_embed_title"], color=discord.Color.red())
    return not_assigned_default_address_embed


def build_current_default_address_embed(default_address: str, lang: str) -> discord.embeds.Embed:
    language_data = get_language_data(lang)

    current_default_address_embed = discord.Embed(title=f"{language_data['current_default_address_embed_title']}`'{default_address}'`", color=discord.Color.green())
    return current_default_address_embed


def build_not_supported_language_embed(supported_languages_str: str, lang: str) -> discord.embeds.Embed:
    language_data = get_language_data(lang)

    not_supported_language_embed = discord.Embed(title=f"{language_data['specified_language_not_supported_embed_title']}`{supported_languages_str}`")
    return not_supported_language_embed


def build_error_embed(lang: str) -> discord.embeds.Embed:
    language_data = get_language_data(lang)

    error_embed = discord.Embed(title=language_data["error_embed_title"], color=discord.Color.red())
    return error_embed
