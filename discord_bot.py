import discord
import logging
import datetime


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

    def check_for_command_identifier(self, message):
        return self.COMMAND_IDENTIFIER == message.content[0]

    # Native Commands

    async def invite(self, message):
        client_id = self.user.id
        discord_api_url = "https://discord.com/api/oauth2/authorize?client_id="
        invite_url = f"{discord_api_url}{client_id}&permissions=0&scope=bot%20applications.commands"

        embed_title = f"Click here to add {self.NAME} to your server!"
        embed_desc = (f"Thanks for your interest in adding {self.NAME} to your server! "
                      f"Please click the link above to proceed.")
        logging.info(f"User {message.author.id} has requested a server invite for {self.NAME}")
        await message.channel.send(embed=self.create_embed(embed_title, embed_desc, invite_url, None))

    async def ping(self, message):
        await message.channel.send("Pong!")

    async def info(self, message):
        embed_title = "Bot Info"
        time_diff = datetime.datetime.utcnow() - self.TIME_START
        embed_desc = (f"Uptime: {time_diff.days} Days, {time_diff.seconds // 3600} Hours, "
                      f"{time_diff.seconds // 60 % 60} Minutes, {time_diff.seconds % 60} Seconds\n"
                      f"Servers Found On: {len(self.guilds)}\n"
                      f"Commands Run Since Start Up: {self.commands_called}")
        await message.channel.send(embed=self.create_embed(embed_title, embed_desc, None, None))

    async def move(self, message):
        # check if sender is in voice channel

        if message.author.voice:
            try:
                await message.mentions[0].edit(voice_channel=message.author.voice.channel)
                embed_title = "Success!"
                embed_desc = f"Moved {message.mentions[0].nick} to voice channel: {message.author.voice.channel.name}"
                await message.channel.send(embed=self.create_embed(embed_title, embed_desc, None, None))
            except discord.Forbidden:
                logging.warning("Bot doesn't have correct permission to move user")
            except Exception as e:
                logging.warning(e)
        else:
            embed_desc = f"{message.author.nick}, please be in a voice channel to use this command"
            await message.channel.send(embed=self.create_embed("Can't move user", embed_desc, None, 0xff0000))

    @staticmethod
    def check_for_bot_message(message):
        return message.author.bot

    def create_embed(self, title_text, desc_text, url,  color_hex):
        if not color_hex:
            color_hex = 0x00ff00
        if not url:
            url = ""
        embed_obj = discord.Embed(title=title_text, description=desc_text, color=color_hex, author=self.NAME, url=url,
                                  name=self.user.name, timestamp=datetime.datetime.utcnow())
        embed_obj.set_footer(text=f"Brought to you by {self.PATRON_URL}", icon_url=self.user.avatar_url)
        return embed_obj
