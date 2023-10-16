import discord
from discord import app_commands
from colorama import Fore
from os import listdir

from functions.server_data_getter import *
from functions.embeds_builders import *
from functions.senders import send_deferred_bot_response
from functions.loggers import log_user_command_message
from functions.interactions_data_processors import *
from functions.icon_saver import *


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
    json_path = "interactions-data.json"

    supported_languages_list = []
    languages_dir = 'languages'
    for filename in listdir(languages_dir):
        normalized_filename = filename.split(".")[0]
        supported_languages_list.append(normalized_filename)

    supported_languages_str = ""
    for language in supported_languages_list:
        supported_languages_str += language + ", "

    supported_languages_str = supported_languages_str[:-2]

    @tree.command(name="help", description="Show the available commands.")
    async def help(interaction: discord.Interaction):
        interaction_lang = get_interaction_language(interaction, json_path)
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            help_embed = build_help_embed(supported_languages_str, interaction_lang)
            await send_deferred_bot_response(interaction, help_embed)

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)

    @tree.command(name="set-default", description="Set the default address that the command '/serverinfo' will use.")
    async def set_default(interaction: discord.Interaction, default_address: str):
        interaction_lang = get_interaction_language(interaction, json_path)
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            data = get_interactions_data(json_path)
            update_interactions_data(interaction, json_path, data, default_address, interaction_lang)

            default_address_embed, file_to_attach = build_default_address_embed(default_address,  interaction_lang)
            await send_deferred_bot_response(interaction, default_address_embed, file_to_attach=file_to_attach)

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)

    @tree.command(name="current-default", description="Returns the current default address.")
    async def current_default(interaction: discord.Interaction):
        interaction_lang = get_interaction_language(interaction, json_path)
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            default_address = get_interaction_default_address(interaction, json_path)
            if default_address is None:
                await send_deferred_bot_response(interaction, build_not_assigned_default_address_embed(interaction_lang))

            else:
                await send_deferred_bot_response(interaction, build_current_default_address_embed(default_address, interaction_lang))

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)

    @tree.command(name="server-info", description="Returns information about a specific server.")
    async def server_info(interaction: discord.Interaction, address: str = ""):
        interaction_lang = get_interaction_language(interaction, json_path)
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            execution_address = get_interaction_default_address(interaction, json_path, address)
            if execution_address == "" or execution_address is None:
                await send_deferred_bot_response(interaction, build_not_assigned_default_address_embed(interaction_lang))

            else:
                server_data = get_minecraft_server_data(execution_address)

                if server_data["online"]:
                    if "icon" in server_data.keys():
                        icon_path = f"server-icons/{execution_address}.png"
                        save_icon(icon_path, server_data["icon"])

                    else:
                        icon_path = "server-icons/default_icon.png"

                    embed_to_send, icon = build_online_server_embed(server_data, execution_address, icon_path, interaction_lang)

                else:
                    embed_to_send, icon = build_unreachable_server_embed(execution_address, interaction_lang)

                await send_deferred_bot_response(interaction, embed_to_send, icon)

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)

    @tree.command(name="language", description="Change the language of the bot.")
    async def language(interaction: discord.Interaction, lang: str):
        interaction_lang = get_interaction_language(interaction, json_path)
        try:
            await interaction.response.defer()
            log_user_command_message(interaction)

            normalized_lang = lang.lower()
            if normalized_lang not in supported_languages_list:
                await send_deferred_bot_response(interaction, build_not_supported_language_embed(supported_languages_str, interaction_lang))

            else:
                data = get_interactions_data(json_path)
                update_interactions_data(interaction, json_path, data, lang=normalized_lang)

                language_embed, file_to_attach = build_language_embed(normalized_lang)
                await send_deferred_bot_response(interaction, language_embed, file_to_attach)

        except Exception as e:
            await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)

    bot.run(token)
