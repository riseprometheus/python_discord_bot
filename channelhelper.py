import discord
import logging
import basicbot


class ChannelHelper:

    @staticmethod
    async def size(client, message, args):
        if await ChannelHelper.is_in_voice_channel(client, message):
            size = 0
            if len(args) >= 3:
                size = int(args[2])
            try:
                await message.author.voice.channel.edit(user_limit=size)
            except discord.Forbidden:
                client.send_missing_permission_warning(message.channel)
                return
            embed_title = "Success!"
            embed_desc = f"Set channel **{message.author.voice.channel.name}** to size ** unlimited**"
            if size > 0:
                embed_desc = f"Set channel **{message.author.voice.channel.name}** to size **{args[2]}**"
            await client.send_embed(channel=message.channel, title=embed_title, description=embed_desc)

    @staticmethod
    async def move(client, message, args):
        # check if sender is in voice channel
        if await ChannelHelper.is_in_voice_channel(client, message):
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
                                        description=embed_desc, color=client.red_hex_color)
            except discord.HTTPException:
                embed_title = "Can't complete action!"
                embed_desc = "Make sure the person to be moved is in a voice channel!"
                await client.send_embed(channel=message.channel, title=embed_title,
                                        description=embed_desc, color=client.red_hex_color)
            except Exception as e:
                logging.warning(e)

    @staticmethod
    async def is_in_voice_channel(client, message):
        if not message.author.voice:
            embed_desc = f"{message.author.nick}, please be in a voice channel to use this command"
            embed_title = "Can't complete command"
            await client.send_embed(channel=message.channel, title=embed_title,
                                    description=embed_desc, color=client.red_hex_color)
            return False
        else:
            return True
