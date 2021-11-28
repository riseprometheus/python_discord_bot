import discord
import logging
import datetime


class MyClient(discord.Client):
    COMMAND_IDENTIFIER = "!"
    NAME = "Trouble Maker"
    PATRON_URL = "ConspiratorSoftworks.xyz"

    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not self.check_for_bot_message(message) and self.check_for_command_identifier(message):
            try:
                function_name = getattr(MyClient, message.content[1:])
                # This should only ever be for bot commands so they should be awaited
                await function_name(self, message)
            except AttributeError:
                pass

    def check_for_command_identifier(self, message):
        return self.COMMAND_IDENTIFIER == message.content[0]

    async def invite(self, message):
        client_id = self.user.id
        discord_api_url = "https://discord.com/api/oauth2/authorize?client_id="
        invite_url = f"{discord_api_url}{client_id}&permissions=0&scope=bot%20applications.commands"

        embed_title = f"Click here to add {self.NAME} to your server!"
        embed_desc = (f"Thanks for your interest in adding {self.NAME} to your server! "
                      f"Please click the link above to proceed.")
        logging.info(f"User {message.author.id} has requested a server invite for {self.NAME}")
        await message.channel.send(embed=self.create_embed(embed_title, embed_desc, invite_url, None))

    @staticmethod
    def check_for_bot_message(message):
        return message.author.bot

    def create_embed(self, title_text, desc_text, url,  color_hex):
        if not color_hex:
            color_hex = 0x00ff00
        embed_obj = discord.Embed(title=title_text, description=desc_text, color=color_hex, author=self.NAME, url=url,
                                  name=self.user.name, timestamp=datetime.datetime.utcnow())
        embed_obj.set_footer(text=f"Brought to you by {self.PATRON_URL}", icon_url=self.user.avatar_url)
        return embed_obj
