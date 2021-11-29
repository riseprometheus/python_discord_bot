import discord
import logging
import datetime

red_hex_color = 0xff0000


class MyClient(discord.Client):
    COMMAND_IDENTIFIER = "!"
    NAME = "Trouble Maker"
    PATRON_URL = "ConspiratorSoftworks.xyz"
    TIME_START = datetime.datetime.utcnow()
    commands_called = 0


    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not self.check_for_bot_message(message) and self.check_for_command_identifier(message):
            try:
                args = message.content[1:].lower().split(" ")
                function_name = getattr(MyClient, args[0])
                # This should only ever be for bot commands so they should be awaited
                await function_name(self, message)
                self.commands_called += 1
            except AttributeError:
                pass

    async def send_embed(self, **kwargs):

        embed_title = kwargs.get("title", "Default Title")
        embed_desc = kwargs.get("description", "Default Description")
        channel = kwargs.get("channel", None)
        url = kwargs.get("url", discord.Embed.Empty)
        color = kwargs.get("color", discord.Embed.Empty)

        try:
            await channel.send(embed=self.create_embed(embed_title, embed_desc, url, color))
        except discord.Forbidden:
            logging.warning("Bot doesn't have correct permission to for this action")
        except Exception as e:
            logging.warning(e)

    def check_for_command_identifier(self, message):
        return self.COMMAND_IDENTIFIER == message.content[0]

    async def is_in_voice_channel(self, message):
        if not message.author.voice:
            embed_desc = f"{message.author.nick}, please be in a voice channel to use this command"
            embed_title = "Can't complete command"
            await self.send_embed(channel=message.channel, title=embed_title,
                                  description=embed_desc, color=red_hex_color)
            return False
        else:
            return True

    # Native Commands

    async def invite(self, message):
        client_id = self.user.id
        discord_api_url = "https://discord.com/api/oauth2/authorize?client_id="
        invite_url = f"{discord_api_url}{client_id}&permissions=0&scope=bot%20applications.commands"

        embed_title = f"Click here to add {self.NAME} to your server!"
        embed_desc = (f"Thanks for your interest in adding {self.NAME} to your server! "
                      f"Please click the link above to proceed.")

        logging.info(f"User {message.author.id} has requested a server invite for {self.NAME}")
        await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc, url=invite_url)

    async def ping(self, message):
        await message.channel.send("Pong!")

    async def info(self, message):
        embed_title = "Bot Info"
        time_diff = datetime.datetime.utcnow() - self.TIME_START
        embed_desc = (f"Uptime: {time_diff.days} Days, {time_diff.seconds // 3600} Hours, "
                      f"{time_diff.seconds // 60 % 60} Minutes, {time_diff.seconds % 60} Seconds\n"
                      f"Servers Found On: {len(self.guilds)}\n"
                      f"Commands Run Since Start Up: {self.commands_called}")
        await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc)

    async def move(self, message):
        # check if sender is in voice channel
        if await self.is_in_voice_channel(message):
            try:
                await message.mentions[0].edit(voice_channel=message.author.voice.channel)
                embed_title = "Success!"
                embed_desc = f"Moved {message.mentions[0].nick} to voice channel: {message.author.voice.channel.name}"
                await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc)
            except discord.Forbidden:
                logging.warning("Bot doesn't have correct permission to for this action")
            except IndexError:
                embed_title = "Missing user to move!"
                embed_desc = "Please tag the person you would to move in your message"
                await self.send_embed(channel=message.channel, title=embed_title,
                                      description=embed_desc, color=red_hex_color)
            except Exception as e:
                logging.warning(e)

    async def size(self, message):
        pass

    @staticmethod
    def check_for_bot_message(message):
        return message.author.bot

    def create_embed(self, title_text, desc_text, url,  color_hex):
        if color_hex == discord.Embed.Empty:
            color_hex = 0x00ff00
        embed_obj = discord.Embed(title=title_text, description=desc_text, color=color_hex, author=self.NAME, url=url,
                                  name=self.user.name, timestamp=datetime.datetime.utcnow())
        embed_obj.set_footer(text=f"Brought to you by {self.PATRON_URL}", icon_url=self.user.avatar_url)
        return embed_obj
