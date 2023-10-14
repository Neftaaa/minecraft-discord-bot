import discord
import json


def update_data_for_guild(interaction: discord.Interaction, data: dict, default_address: str) -> dict:
    guilds_list = data["guilds"]
    is_new_guild = True
    guild_id = interaction.guild.id

    for guild in guilds_list:
        if guild["guild_id"] == guild_id:
            guild["default_address"] = default_address
            is_new_guild = False

    if is_new_guild:
        guild_info = {"guild_id": guild_id, "default_address": default_address}
        guild_list.append(guild_info)

    data["guilds"] = guilds_list
    return data


def update_data_for_private(interaction: discord.Interaction, data: dict, default_address: str) -> dict:
    privates_list = data["privates"]
    is_new_user = True
    user_id = interaction.user.id

    for private in privates_list:
        if private["user_id"] == user_id:
            private["default_address"] = default_address
            is_new_user = False

    if is_new_user:
        private_info = {"user_id": user_id, "default_address": default_address}
        privates_list.append(private_info)

    data["privates"] = privates_list
    return data


def get_data_from_json(file_path: str) -> dict:
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def update_json_data(interaction: discord.Interaction, data, default_address, file_path: str):
    if str(interaction.channel.type) == "text":
        updated_data = update_data_for_guild(interaction, data, default_address)

    elif str(interaction.channel.type) == "private":
        updated_data = update_data_for_private(interaction, data, default_address)

    else:
        return

    with open(file_path, "w") as json_file:
        json.dump(updated_data, json_file)


def get_remote_minecraft_address(interaction: discord.Interaction, json_path: str, server_address: str | None = None) -> str | None:
    if server_address == "" or server_address is None:
        data = get_data_from_json(json_path)

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
