import json
from datetime import datetime
import minestat
from colorama import Fore
import discord
import discord.ext
from discord import app_commands


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

    async def send_bot_response(interaction: discord.Interaction, message_to_send: str | discord.embeds.Embed | None = None,
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

    def get_data_from_json(file_path: str = json_path):
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

    def build_online_server_embed(ms: minestat.MineStat, address, favicon_url: str) -> (discord.embeds.Embed, None):
        server_info_embed = discord.Embed(title="**Server information :**", color=discord.Color.green())

        server_info_embed.set_author(name=address, icon_url=favicon_url)
        server_info_embed.set_thumbnail(url=favicon_url)

        server_info_embed.add_field(name="MOTD:", value=ms.stripped_motd, inline=False)
        server_info_embed.add_field(name="\u200B", value="\u200B", inline=False)
        server_info_embed.add_field(name="Player(s):", value=f"{ms.current_players}/{ms.max_players}", inline=True)
        server_info_embed.add_field(name="Ping:", value=f"{ms.latency}ms", inline=True)
        server_info_embed.add_field(name="Version:", value=ms.version, inline=True)

        server_info_embed.timestamp = datetime.now()
        server_info_embed.set_footer(text="\u200B", icon_url=favicon_url)
        return server_info_embed, None

    def build_unreachable_server_embed(address) -> (discord.embeds.Embed, discord.File):
        error_image = discord.File("resources/error.png", filename="error.png")

        server_info_embed = discord.Embed(title="**Can't connect to server.**", color=discord.Color.green())

        server_info_embed.add_field(name="", value="Server is offline or doesn't exist.")

        server_info_embed.set_author(name=address, icon_url="attachment://error.png")
        server_info_embed.set_thumbnail(url="attachment://error.png")

        server_info_embed.timestamp = datetime.now()
        server_info_embed.set_footer()
        return server_info_embed, error_image

    def get_minecraft_server_info(address: str) -> (minestat.MineStat | None, str | None):
        ms = minestat.MineStat(address, 25565)

        if ms.online:
            favicon_url = f"https://eu.mc-api.net/v3/server/favicon/{address}"
            return ms, favicon_url
        else:
            return ms, None

    """
    @bot.command()
    async def serverhelp(ctx: commands.Context):
        help_embed = discord.Embed(title="Help", color=discord.Color.green())
    """

    @tree.command(name="setdefault", description="Set the default address that the command '/serverinfo' will use.")
    async def setdefault(interaction: discord.Interaction, default_address: str):
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            guild_info = {
                "guild_id": interaction.guild.id,
                "default_address": default_address
            }

            data = get_data_from_json(json_path)

            for data_object in data:
                if guild_info["guild_id"] == data_object["guild_id"]:
                    data_object["default_address"] = guild_info["default_address"]

                    update_json_data(data)
                    await send_bot_response(interaction, f"Default address assigned: '{default_address}'")
                    return

            data.append(guild_info)
            update_json_data(data)

            await send_bot_response(interaction, f"Default address assigned: '{default_address}'")

        except Exception as e:
            await send_bot_response(interaction, exception=e)

    @tree.command(name="serverinfo", description="Returns information about a specific server.")
    async def serverinfo(interaction: discord.Interaction, address: str = ""):
        log_user_command_message(interaction)
        try:
            await interaction.response.defer()
            execution_address = get_remote_minecraft_address(interaction.guild.id, address)
            if execution_address == "" or execution_address is None:
                await send_bot_response(interaction, "Default address is not assigned. Use /setdefault 'address' to assign it.")

            else:
                server_info, favicon_url = get_minecraft_server_info(execution_address)
                if server_info.online:
                    embed_to_send, file_to_attach = build_online_server_embed(server_info, execution_address, favicon_url)

                else:
                    embed_to_send, file_to_attach = build_unreachable_server_embed(execution_address)

                await send_bot_response(interaction, embed_to_send, file_to_attach)

        except Exception as e:
            await send_bot_response(interaction, exception=e)

    bot.run(token)
