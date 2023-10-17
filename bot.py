import discord
from discord import app_commands
from colorama import Fore

from functions.init import *
from commands import *


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

    bot = Client()
    tree = app_commands.CommandTree(bot)
    json_path = "interactions-data.json"

    token = get_bot_token()
    supported_languages_list, supported_languages_str = get_supported_languages()

    @tree.command(name="help", description="Show the available commands.")
    async def help(interaction: discord.Interaction):
        await help_command(interaction, supported_languages_str, json_path)

    @tree.command(name="set-default", description="Set the default address that the command '/serverinfo' will use.")
    async def set_default(interaction: discord.Interaction, default_address: str):
        await set_default_command(interaction, default_address, json_path)

    @tree.command(name="current-default", description="Returns the current default address.")
    async def current_default(interaction: discord.Interaction):
        await current_default_command(interaction, json_path)

    @tree.command(name="server-info", description="Returns information about a specific server.")
    async def server_info(interaction: discord.Interaction, address: str = ""):
        await server_info_command(interaction, json_path, address)

    @tree.command(name="language", description="Change the language of the bot.")
    async def language(interaction: discord.Interaction, lang: str):
        await language_command(interaction, lang, supported_languages_list, supported_languages_str, json_path)

    bot.run(token)
