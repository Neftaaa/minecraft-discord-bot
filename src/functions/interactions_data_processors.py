import discord
import json
from os import path


def get_interactions_data(file_path: str) -> dict:
    if path.exists(file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    with open(file_path, "w+") as interaction_data_file:
        interaction_data_file.write('{"guilds": [], "privates": []}')
        return {"guilds": [], "privates": []}


def get_language_data(lang: str):
    filepath = f"languages/{lang}.json"

    with open(filepath, "r", encoding="utf-8") as language_file:
        return json.load(language_file)


def get_interaction_language(interaction: discord.Interaction, file_path: str) -> str:
    data = get_interactions_data(file_path)

    if str(interaction.channel.type) == "private":
        privates_list = data["privates"]
        user_id = interaction.user.id

        for private in privates_list:
            if user_id == private["user_id"]:
                return private["lang"]

    else:
        guilds_list = data["guilds"]
        guild_id = interaction.guild.id

        for guild in guilds_list:
            if guild_id == guild["guild_id"]:
                return guild["lang"]

    return "en"


def get_interaction_default_address(interaction: discord.Interaction, json_path: str, server_address: str | None = None) -> str | None:
    if server_address == "" or server_address is None:
        data = get_interactions_data(json_path)

        if str(interaction.channel.type) == "private":
            privates_list = data["privates"]
            user_id = interaction.user.id

            for private in privates_list:
                if user_id == private["user_id"]:
                    return private["default_address"]

        else:
            guilds_list = data["guilds"]
            guild_id = interaction.guild.id

            for guild in guilds_list:
                if guild_id == guild["guild_id"]:
                    return guild["default_address"]

        return None

    return server_address


def update_interactions_data_for_guild(interaction: discord.Interaction, data: dict, default_address: str | None, lang: str | None) -> dict:
    guilds_list = data["guilds"]
    is_new_guild = True
    guild_id = interaction.guild.id

    for guild in guilds_list:
        if guild["guild_id"] == guild_id:
            if default_address is not None:
                guild["default_address"] = default_address

            if lang is not None:
                guild["lang"] = lang

            is_new_guild = False

    if is_new_guild:
        if lang is None:
            lang = "en"

        guild_info = {"guild_id": guild_id, "default_address": default_address, "lang": lang}
        guilds_list.append(guild_info)

    data["guilds"] = guilds_list
    return data


def update_interactions_data_for_private(interaction: discord.Interaction, data: dict, default_address: str | None, lang: str | None) -> dict:
    privates_list = data["privates"]
    is_new_user = True
    user_id = interaction.user.id

    for private in privates_list:
        if private["user_id"] == user_id:
            if default_address is not None:
                private["default_address"] = default_address
            if lang is not None:
                private["lang"] = lang
            else:
                private["lang"] = "en"

            is_new_user = False

    if is_new_user:
        private_info = {"user_id": user_id, "default_address": default_address, "lang": lang}
        privates_list.append(private_info)

    data["privates"] = privates_list
    return data


def update_interactions_data(interaction: discord.Interaction, file_path: str, data: dict, default_address: str | None = None, lang: str | None = None):
    if str(interaction.channel.type) == "text":
        updated_data = update_interactions_data_for_guild(interaction, data, default_address, lang)

    elif str(interaction.channel.type) == "private":
        updated_data = update_interactions_data_for_private(interaction, data, default_address, lang)

    else:
        return

    with open(file_path, "w") as json_file:
        json.dump(updated_data, json_file)
