import discord
from loggers import *


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