import discord
from datetime import datetime


def convert_server_info_dict(server_info: dict) -> dict:
    motd = server_info["motd"]
    clean_motd = motd["clean"]
    if len(clean_motd) == 1:
        usable_motd = clean_motd[0]
    else:
        usable_motd = f"{clean_motd[0]}\n{clean_motd[1]}"

    players_info = server_info["players"]
    online_player_count = players_info["online"]
    max_player_count = players_info["max"]

    version = server_info["version"]
    return {"final_motd": usable_motd, "online_player_count": online_player_count,
            "max_player_count": max_player_count, "version": version}


def build_help_embed():
    help_embed = discord.Embed(title="Help", color=discord.Color.green())
    help_embed.add_field(name="Bot information:", value="```MC Server Info is a discord bot that returns information about a minecraft server.```", inline=False)
    help_embed.add_field(name="/help", value="```Show this message.```", inline=False)
    help_embed.add_field(name="/serverinfo `address`", value="```Will return information about a specific minecraft server. Can be use without specifying the address if you set"
                                                             " a default address with '/setdefault'.```", inline=False)
    help_embed.add_field(name="/setdefault `default_address`", value="```Set a default address that the bot will use if you don't specify an address using '/serverinfo'.```",
                         inline=False)
    return help_embed


def build_online_server_embed(server_info: dict, address, favicon_url: str) -> (discord.embeds.Embed, None):
    usable_server_info = convert_server_info_dict(server_info)

    server_info_embed = discord.Embed(title="Server information :", color=discord.Color.green())

    server_info_embed.set_author(name=address, icon_url=favicon_url)
    server_info_embed.set_thumbnail(url=favicon_url)

    server_info_embed.add_field(name="MOTD:", value=f"```{usable_server_info['final_motd']}```", inline=False)
    server_info_embed.add_field(name="\u200B", value="\u200B", inline=False)
    server_info_embed.add_field(name="Status:", value=f"`Online`", inline=True)
    server_info_embed.add_field(name="Player(s):", value=f"`{usable_server_info['online_player_count']}"
                                                         f"/{usable_server_info['max_player_count']}`", inline=True)
    server_info_embed.add_field(name="Version:", value=f"`{usable_server_info['version']}`", inline=True)

    server_info_embed.timestamp = datetime.now()
    server_info_embed.set_footer(text="\u200B", icon_url=favicon_url)
    return server_info_embed, None


def build_unreachable_server_embed(address) -> (discord.embeds.Embed, discord.File):
    error_image = discord.File("resources/error.png", filename="error.png")

    server_info_embed = discord.Embed(title="Can't connect to server.", color=discord.Color.red())

    server_info_embed.add_field(name="", value="`Server is offline or doesn't exist.`")

    server_info_embed.set_author(name=address, icon_url="attachment://error.png")
    server_info_embed.set_thumbnail(url="attachment://error.png")

    server_info_embed.timestamp = datetime.now()
    server_info_embed.set_footer()
    return server_info_embed, error_image


def build_default_address_embed(default_address: str) -> (discord.embeds.Embed, discord.File):
    valid_image = discord.File("resources/valid.png", filename="valid.png")

    default_address_embed = discord.Embed(title=f"Default address assigned: '{default_address}'", color=discord.Color.green())
    default_address_embed.set_author(name=default_address, icon_url="attachment://valid.png")
    default_address_embed.set_thumbnail(url="attachment://valid.png")

    default_address_embed.timestamp = datetime.now()
    default_address_embed.set_footer()
    return default_address_embed, valid_image
