import discord
import logging
import discord_bot


class ChannelHelper:

    @staticmethod
    async def size(client, message, args):
        if await client.is_in_voice_channel(message):
            try:
                await message.author.voice.channel.edit(user_limit=args[2])
            except discord.Forbidden:
                client.send_missing_permission_warning(message.channel)
                return
            embed_title = "Success!"
            embed_desc = f"Set channel: **{message.author.voice.channel.name}** to size **{args[2]}**"
            await client.send_embed(channel=message.channel, title=embed_title, description=embed_desc)

    @staticmethod
    async def move(client, message, args):
        # check if sender is in voice channel
        if await client.is_in_voice_channel(message):
            try:
                await message.mentions[0].edit(voice_channel=message.author.voice.channel)
                embed_title = "Success!"
                embed_desc = f"Moved {message.mentions[0].nick} to voice channel: {message.author.voice.channel.name}"
                await client.send_embed(channel=message.channel, title=embed_title, description=embed_desc)
            except discord.Forbidden:
                client.send_missing_permission_warning(message.channel)
                return
            except IndexError:
                embed_title = "Missing user to move!"
                embed_desc = "Please tag the person you would to move in your message"
                await client.send_embed(channel=message.channel, title=embed_title,
                                        description=embed_desc, color=discord_bot.red_hex_color)
            except Exception as e:
                logging.warning(e)
