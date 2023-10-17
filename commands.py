from functions.server_data_getter import *
from functions.embeds_builders import *
from functions.senders import send_deferred_bot_response
from functions.loggers import log_user_command_message
from functions.interactions_data_processors import *
from functions.icon_saver import *


async def help_command(interaction: discord.Interaction, supported_languages_str: str, json_path: str):
    interaction_lang = get_interaction_language(interaction, json_path)
    try:
        await interaction.response.defer()
        log_user_command_message(interaction)

        help_embed = build_help_embed(supported_languages_str, interaction_lang)
        await send_deferred_bot_response(interaction, help_embed)

    except Exception as e:
        await send_deferred_bot_response(interaction, exception=e, lang=interaction_lang)


async def set_default_command(interaction: discord.Interaction, default_address: str, json_path: str):
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


async def current_default_command(interaction: discord.Interaction, json_path: str):
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


async def server_info_command(interaction: discord.Interaction, json_path: str, address: str = ""):
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


async def language_command(interaction: discord.Interaction, lang: str, supported_languages_list: list, supported_languages_str: str, json_path: str):
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
