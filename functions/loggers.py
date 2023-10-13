import discord
from colorama import Fore


def log_user_command_message(interaction: discord.Interaction):

    username = str(interaction.user.name)
    command = str(interaction.command.name)
    channel = str(interaction.channel)

    if str(interaction.channel.type) == "private":
        user = interaction.user
        user_id = interaction.user.id

        print(f"Private: {Fore.LIGHTYELLOW_EX}{user} {Fore.MAGENTA}({user_id}){Fore.RESET}: {Fore.CYAN}{username}{Fore.RESET} used command: {Fore.LIGHTGREEN_EX}'{command}'"
              f" {Fore.BLUE}({channel}){Fore.RESET}")

    else:
        guild = str(interaction.guild.name)
        guild_id = str(interaction.guild.id)

        print(f"Guild: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: {Fore.CYAN}{username}{Fore.RESET} used command: {Fore.LIGHTGREEN_EX}'{command}'"
              f"{Fore.RESET} {Fore.BLUE}({channel}){Fore.RESET}")


def log_bot_response(interaction: discord.Interaction, exception: Exception | None = None):

    bot = str(interaction.client.user)
    username = str(interaction.user.name)
    command = str(interaction.command.name)
    channel = str(interaction.channel)

    if str(interaction.channel.type) == "private":
        user = interaction.user
        user_id = interaction.user.id

        if exception is None:
            print(f"Private: {Fore.LIGHTYELLOW_EX}{user} {Fore.MAGENTA}({user_id}){Fore.RESET}: {Fore.GREEN}{bot}{Fore.RESET} answered successfully to {Fore.CYAN}{username}"
                  f"{Fore.RESET} {Fore.LIGHTGREEN_EX}'{command}' {Fore.BLUE}({channel}){Fore.RESET}{Fore.RESET}")

        else:
            print(f"Private: {Fore.LIGHTYELLOW_EX}{user} {Fore.MAGENTA}({user_id}){Fore.RESET}: {Fore.GREEN}{bot}{Fore.RESET} failed to respond to {Fore.CYAN}{username}\n    "
                  f"{Fore.LIGHTRED_EX}Exception: {exception}{Fore.RESET}")

    else:
        guild = str(interaction.guild.name)
        guild_id = str(interaction.guild.id)

        if exception is None:
            print(f"Guild: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: {Fore.GREEN}{bot}{Fore.RESET} answered successfully to {Fore.CYAN}{username}"
                  f"{Fore.RESET} {Fore.LIGHTGREEN_EX}'{command}' {Fore.BLUE}({channel}){Fore.RESET}{Fore.RESET}")

        else:
            print(f"Guild: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: {Fore.GREEN}{bot}{Fore.RESET} failed to respond to {Fore.CYAN} {Fore.BLUE}"
                  f"({channel}){Fore.RESET}\n    {Fore.LIGHTRED_EX}Exception: {exception}{Fore.RESET}")
