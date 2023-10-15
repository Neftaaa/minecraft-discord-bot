import discord
from datetime import datetime


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


def build_help_embed(supported_languages: str) -> discord.embeds.Embed:
    help_embed = discord.Embed(title="Help", color=discord.Color.green())
    help_embed.add_field(name="Bot information:", value="```MC Server Info is a discord bot that returns information about a minecraft server.```", inline=False)
    help_embed.add_field(name="/help", value="```Show this message.```", inline=False)
    help_embed.add_field(name="/server-info `address`", value="```Will return information about a specific minecraft server. Can be use without specifying the address if you set"
                                                              " a default address with '/set-default'.```", inline=False)
    help_embed.add_field(name="/set-default `default_address`", value="```Set a default address that the bot will use if you don't specify an address using '/server-info'.```",
                         inline=False)
    help_embed.add_field(name="/current-default", value="```Returns the current default address.```")
    help_embed.add_field(name="/language", value=f"```Change the language of the bot. Supported languages: {supported_languages}.```")
    return help_embed


def build_online_server_embed(server_data: dict, address, icon_path: str) -> (discord.embeds.Embed, discord.File):
    usable_server_data = convert_server_data_dict(server_data)
    server_icon = discord.File(icon_path, filename="default_icon.png")

    server_data_embed = discord.Embed(title="Server information :", color=discord.Color.green())

    server_data_embed.set_author(name=address, icon_url="attachment://default_icon.png")
    server_data_embed.set_thumbnail(url="attachment://default_icon.png")

    server_data_embed.add_field(name="MOTD:", value=f"```{usable_server_data['final_motd']}```", inline=False)
    server_data_embed.add_field(name="\u200B", value="\u200B", inline=False)
    server_data_embed.add_field(name="Status:", value=f"`Online`", inline=True)
    server_data_embed.add_field(name="Player(s):", value=f"`{usable_server_data['online_player_count']}"
                                                         f"/{usable_server_data['max_player_count']}`", inline=True)
    server_data_embed.add_field(name="Version:", value=f"`{usable_server_data['version']}`", inline=True)

    server_data_embed.timestamp = datetime.now()
    server_data_embed.set_footer(text="\u200B", icon_url="attachment://default_icon.png")
    return server_data_embed, server_icon


def build_unreachable_server_embed(address) -> (discord.embeds.Embed, discord.File):
    error_image = discord.File("resources/error.png", filename="error.png")

    server_data_embed = discord.Embed(title="Can't connect to server.", color=discord.Color.red())

    server_data_embed.add_field(name="", value="`Server is offline or doesn't exist.`")

    server_data_embed.set_author(name=address, icon_url="attachment://error.png")
    server_data_embed.set_thumbnail(url="attachment://error.png")

    server_data_embed.timestamp = datetime.now()
    server_data_embed.set_footer()
    return server_data_embed, error_image


def build_default_address_embed(default_address: str) -> (discord.embeds.Embed, discord.File):
    valid_image = discord.File("resources/valid.png", filename="valid.png")

    default_address_embed = discord.Embed(title=f"Default address assigned: '{default_address}'", color=discord.Color.green())
    default_address_embed.set_author(name=default_address, icon_url="attachment://valid.png")
    default_address_embed.set_thumbnail(url="attachment://valid.png")

    default_address_embed.timestamp = datetime.now()
    default_address_embed.set_footer()
    return default_address_embed, valid_image


def build_language_embed(lang: str) -> (discord.embeds.Embed, discord.File):
    valid_image = discord.File("resources/valid.png", filename="valid.png")

    default_address_embed = discord.Embed(title=f"Language assigned: '{lang}'", color=discord.Color.green())
    default_address_embed.set_author(name=lang, icon_url="attachment://valid.png")
    default_address_embed.set_thumbnail(url="attachment://valid.png")

    default_address_embed.timestamp = datetime.now()
    default_address_embed.set_footer()
    return default_address_embed, valid_image
