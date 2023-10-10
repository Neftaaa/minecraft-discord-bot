import json
from datetime import datetime
from colorama import Fore
import discord
from discord import app_commands
import requests


def run_discord_bot():
    class Client(discord.Client):
        def __init__(self) -> None:
            intents = discord.Intents.all()

            super().__init__(intents=intents)
            self.synced = False

        async def on_ready(self):
            await self.wait_until_ready()
            if not self.synced:
                await tree.sync()
                self.synced = True

            print(f'{Fore.GREEN}{bot.user}{Fore.RESET} is now running!{Fore.RESET}')

    with open("token.txt", "r") as token_file:
        token = token_file.read()

    bot = Client()
    tree = app_commands.CommandTree(bot)
    json_path = "info.json"

    def log_user_command_message(interaction: discord.Interaction):

        username = str(interaction.user)
        command = str(interaction.command.name)
        channel = str(interaction.channel)
        guild = str(interaction.guild.name)
        guild_id = str(interaction.guild.id)

        print(f"Server: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: "
              f"{Fore.CYAN}{username}{Fore.RESET} used command: {Fore.LIGHTGREEN_EX}'{command}'{Fore.RESET} "
              f"{Fore.BLUE}({channel}){Fore.RESET}")

    def log_bot_response(interaction: discord.Interaction, exception: Exception | None = None):

        username = str(interaction.user)
        command = str(interaction.command.name)
        channel = str(interaction.channel)
        guild = str(interaction.guild.name)
        guild_id = str(interaction.guild.id)

        if exception is None:
            print(f"Server: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: "
                  f"{Fore.GREEN}{bot.user}{Fore.RESET} answered successfully to {Fore.CYAN}{username}{Fore.RESET} "
                  f"command: {Fore.LIGHTGREEN_EX}'{command}' {Fore.BLUE}({channel}){Fore.RESET}{Fore.RESET}")

        else:
            print(f"Server: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: "
                  f"{Fore.GREEN}{bot.user}{Fore.RESET} failed to respond to {Fore.CYAN} "
                  f"{Fore.BLUE}({channel}){Fore.RESET}\n"
                  f"    {Fore.LIGHTRED_EX}Exception: {exception}{Fore.RESET}")

    async def send_deferred_bot_response(interaction: discord.Interaction, message_to_send: str | discord.embeds.Embed | None = None,
                                         file_to_attach: discord.file.File | None = None, exception: Exception | None = None):
        if exception is not None:
            log_bot_response(interaction, exception)
            await interaction.followup.send("An error occurred.")

        else:
            try:
                if type(message_to_send) == str:
                    await interaction.followup.send(message_to_send)
                    log_bot_response(interaction)

                else:
                    if file_to_attach is not None:
                        await interaction.followup.send(embed=message_to_send, file=file_to_attach)
                    else:
                        await interaction.followup.send(embed=message_to_send)
                    log_bot_response(interaction)

            except Exception as e:
                log_bot_response(interaction, e)

    async def send_bot_response(interaction: discord.Interaction, message_to_send: str | discord.embeds.Embed | None = None,
                                file_to_attach: discord.file.File | None = None, exception: Exception | None = None):
        if exception is not None:
            log_bot_response(interaction, exception)
            await interaction.response.send_message("An error occurred.")

        else:
            try:
                if type(message_to_send) == str:
                    await interaction.response.send_message(message_to_send)
                    log_bot_response(interaction)

                else:
                    if file_to_attach is not None:
                        await interaction.response.send_message(embed=message_to_send, file=file_to_attach)
                    else:
                        await interaction.response.send_message(embed=message_to_send)
                    log_bot_response(interaction)

            except Exception as e:
                log_bot_response(interaction, e)

    def get_data_from_json(file_path: str = json_path) -> list:
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    def update_json_data(data, file_path: str = json_path):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    def get_remote_minecraft_address(server_id: int, command_address: str) -> str | None:
        if command_address == "" or command_address is None:
            data = get_data_from_json(json_path)

            for data_objet in data:
                if server_id == data_objet["guild_id"]:
                    return data_objet["default_address"]

            return None

        return command_address

    def get_minecraft_server_info(address: str) -> (dict, str | None):
        server_info_request = requests.get(f"https://api.mcsrvstat.us/3/{address}")
        server_info = server_info_request.json()

        if server_info["online"]:
            icon_url = f"https://api.mcsrvstat.us/icon/{address}"
            return server_info, icon_url
        else:
            return server_info, None

    def convert_server_info_dict(server_info: dict) -> dict:
        motd = server_info["motd"]
        clean_motd = motd["clean"]
        if len(clean_motd) == 1:
            final_motd = clean_motd[0]
        else:
            final_motd = f"{clean_motd[0]}\n{clean_motd[1]}"

        players_info = server_info["players"]
        online_player_count = players_info["online"]
        max_player_count = players_info["max"]

        version = server_info["version"]
        return {"final_motd": final_motd, "online_player_count": online_player_count,
                "max_player_count": max_player_count, "version": version}

    def build_online_server_embed(server_info: dict, address, favicon_url: str) -> (discord.embeds.Embed, None):

        usable_server_info = convert_server_info_dict(server_info)

        server_info_embed = discord.Embed(title="Server information :", color=discord.Color.green())

        server_info_embed.set_author(name=address, icon_url=favicon_url)
        server_info_embed.set_thumbnail(url=favicon_url)

        server_info_embed.add_field(name="MOTD:", value=usable_server_info["final_motd"], inline=False)
        server_info_embed.add_field(name="\u200B", value="\u200B", inline=False)
        server_info_embed.add_field(name="Status:", value=f"Online", inline=True)
        server_info_embed.add_field(name="Player(s):", value=f"{usable_server_info['online_player_count']}"
                                                             f"/{usable_server_info['max_player_count']}", inline=True)
        server_info_embed.add_field(name="Version:", value=usable_server_info['version'], inline=True)

        server_info_embed.timestamp = datetime.now()
        server_info_embed.set_footer(text="\u200B", icon_url=favicon_url)
        return server_info_embed, None

    def build_unreachable_server_embed(address) -> (discord.embeds.Embed, discord.File):
        error_image = discord.File("resources/error.png", filename="error.png")

        server_info_embed = discord.Embed(title="Can't connect to server.", color=discord.Color.green())

        server_info_embed.add_field(name="", value="Server is offline or doesn't exist.")

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

    def build_help_embed():
        help_embed = discord.Embed(title="Help", color=discord.Color.green())
        help_embed.add_field(name="Bot information:", value="MC Server Info is a discord bot that returns information about a minecraft server.", inline=False)
        help_embed.add_field(name="/help", value="Show this message.", inline=False)
        help_embed.add_field(name="/serverinfo 'address'", value="Will return information about a specific minecraft server. Can be use without specifying the address if you set"
                                                                 " a default address with '/setdefault'.", inline=False)
        help_embed.add_field(name="/setdefault 'default_address'", value="Set a default address that the bot will use if you don't specify an address using '/serverinfo'.",
                             inline=False)
        return help_embed

    @tree.command(name="help", description="Show the available commands.")
    async def help(interaction: discord.Interaction):
        help_embed = build_help_embed()
        await send_bot_response(interaction, help_embed)

    @tree.command(name="setdefault", description="Set the default address that the command '/serverinfo' will use.")
    async def setdefault(interaction: discord.Interaction, default_address: str):
        try:
            log_user_command_message(interaction)

            default_address_embed, file_to_attach = build_default_address_embed(default_address)

            guild_info = {
                "guild_id": interaction.guild.id,
                "default_address": default_address
            }

            data = get_data_from_json(json_path)

            for data_object in data:
                if guild_info["guild_id"] == data_object["guild_id"]:
                    data_object["default_address"] = guild_info["default_address"]

                    update_json_data(data)
                    await send_bot_response(interaction, default_address_embed, file_to_attach=file_to_attach)
                    return

            data.append(guild_info)
            update_json_data(data)

            await send_bot_response(interaction, default_address_embed, file_to_attach=file_to_attach)

        except Exception as e:
            await send_bot_response(interaction, exception=e)

    @tree.command(name="serverinfo", description="Returns information about a specific server.")
    async def serverinfo(interaction: discord.Interaction, address: str = ""):
        log_user_command_message(interaction)
        try:
            await interaction.response.defer()
            execution_address = get_remote_minecraft_address(interaction.guild.id, address)
            if execution_address == "" or execution_address is None:
                await send_deferred_bot_response(interaction, "Default address is not assigned. Use /setdefault 'address' to assign it.")

            else:
                server_info, icon_url = get_minecraft_server_info(execution_address)
                if icon_url is None:
                    embed_to_send, file_to_attach = build_unreachable_server_embed(execution_address)

                else:
                    embed_to_send, file_to_attach = build_online_server_embed(server_info, execution_address, icon_url)

                await send_deferred_bot_response(interaction, embed_to_send, file_to_attach)

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e)

    bot.run(token)
