import discord
from colorama import Fore


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

    bot = str(interaction.client.user)
    username = str(interaction.user)
    command = str(interaction.command.name)
    channel = str(interaction.channel)
    guild = str(interaction.guild.name)
    guild_id = str(interaction.guild.id)

    if exception is None:
        print(f"Server: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: "
              f"{Fore.GREEN}{bot}{Fore.RESET} answered successfully to {Fore.CYAN}{username}{Fore.RESET} "
              f"command: {Fore.LIGHTGREEN_EX}'{command}' {Fore.BLUE}({channel}){Fore.RESET}{Fore.RESET}")

    else:
        print(f"Server: {Fore.LIGHTYELLOW_EX}{guild} {Fore.MAGENTA}({guild_id}){Fore.RESET}: "
              f"{Fore.GREEN}{bot}{Fore.RESET} failed to respond to {Fore.CYAN} "
              f"{Fore.BLUE}({channel}){Fore.RESET}\n"
              f"    {Fore.LIGHTRED_EX}Exception: {exception}{Fore.RESET}")
