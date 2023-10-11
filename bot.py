import discord
from discord import app_commands

from functions.server_info_getter import get_minecraft_server_info
from functions.embeds_builders import *
from functions.senders import *
from functions.json_files_processors import *


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

    @tree.command(name="help", description="Show the available commands.")
    async def help(interaction: discord.Interaction):
        log_user_command_message(interaction)

        help_embed = build_help_embed()
        await send_bot_response(interaction, help_embed)

    @tree.command(name="setdefault", description="Set the default address that the command '/serverinfo' will use.")
    async def setdefault(interaction: discord.Interaction, default_address: str):
        log_user_command_message(interaction)
        try:

            data = get_data_from_json(json_path)
            update_json_data(interaction, data, default_address, json_path)

            default_address_embed, file_to_attach = build_default_address_embed(default_address)
            await send_bot_response(interaction, default_address_embed, file_to_attach=file_to_attach)

        except Exception as e:
            await send_bot_response(interaction, exception=e)

    @tree.command(name="serverinfo", description="Returns information about a specific server.")
    async def serverinfo(interaction: discord.Interaction, address: str = ""):
        log_user_command_message(interaction)
        try:
            await interaction.response.defer()
            execution_address = get_remote_minecraft_address(interaction, address, json_path)
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
