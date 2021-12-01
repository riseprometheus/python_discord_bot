import discord
import logging
import datetime
import channelhelper



class MyClient(discord.Client):
    DEFAULT_COMMAND_IDENTIFIER = "!"
    command_identifier = DEFAULT_COMMAND_IDENTIFIER
    NAME = "Trouble Maker"
    PATRON_URL = "ConspiratorSoftworks.xyz"
    TIME_START = datetime.datetime.utcnow()
    optional_modules = []
    commands_called = 0
    bot_embed_title_map = {
        'setup': "Setting up bot configuration"
    }
    red_hex_color = 0xff0000

    module_map = {
        "voice": channelhelper.ChannelHelper()
    }

    async def on_ready(self):
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):

        if self.check_if_embed_needs_response(message):
            self.process_bot_embeds(message)

        if not self.check_for_bot_message(message) and self.check_for_command_identifier(message):
            try:
                args = message.content[1:].lower().split(" ")
                if args[0] in self.module_map:
                    if len(args) < 2:
                        await self.send_embed(channel=message.channel, title="Bad", description="**Nope**",
                                              color=self.red_hex_color)
                        return
                    function_name = getattr(self.module_map[args[0]], args[1], None)
                else:
                    function_name = getattr(MyClient, args[0], None)
                if function_name:
                    await function_name(self, message, args)
                    self.commands_called += 1
            except (AttributeError, TypeError) as e:
                logging.error(e)
            except Exception as e:
                logging.error(e)

    # Native Commands

    async def invite(self, message, args):
        client_id = self.user.id
        discord_api_url = "https://discord.com/api/oauth2/authorize?client_id="
        invite_url = f"{discord_api_url}{client_id}&permissions=0&scope=bot%20applications.commands"

        embed_title = f"Click here to add {self.NAME} to your server!"
        embed_desc = (f"Thanks for your interest in adding {self.NAME} to your server! "
                      f"Please click the link above to proceed.")

        logging.info(f"User {message.author.id} has requested a server invite for {self.NAME}")
        await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc, url=invite_url)

    async def ping(self, message, args):
        await message.channel.send("Pong!")

    async def info(self, message, args):
        embed_title = "Bot Info"
        time_diff = datetime.datetime.utcnow() - self.TIME_START
        embed_desc = (f"**Uptime**: {time_diff.days} Days, {time_diff.seconds // 3600} Hours, "
                      f"{time_diff.seconds // 60 % 60} Minutes, {time_diff.seconds % 60} Seconds\n"
                      f"**Servers Found On:** {len(self.guilds)}\n"
                      f"**Commands Run Since Start Up**: {self.commands_called}")
        await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc)

    async def setup(self, message, args):
        embed_title = self.bot_embed_title_map["setup"]
        embed_desc = (f"First lets select your command identifier\n"
                      f"Run **{self.command_identifier}set identifier <Your chosen identifier>**\n"
                      f"Note: this identifier can't be a number or letter")
        await self.send_embed(channel=message.channel, title=embed_title, description=embed_desc)

    # Helpers

    def check_if_embed_needs_response(self, message):
        # Check is message originated from this bot and is in bot_embed_title_map.values()
        return message.author.id == self.user.id and len(message.embeds) > 0 and \
               message.embeds[0].title in self.bot_embed_title_map.values()

    @staticmethod
    def check_for_bot_message(message):
        return message.author.bot

    def create_embed(self, title_text, desc_text, url, color_hex):
        if color_hex == discord.Embed.Empty:
            color_hex = 0x00ff00
        embed_obj = discord.Embed(title=title_text, description=desc_text, color=color_hex, author=self.NAME, url=url,
                                  name=self.user.name, timestamp=datetime.datetime.utcnow())
        embed_obj.set_footer(text=f"Brought to you by {self.PATRON_URL}", icon_url=self.user.avatar_url)
        return embed_obj

    async def send_embed(self, **kwargs):
        embed_title = kwargs.get("title", "Default Title")
        embed_desc = kwargs.get("description", "Default Description")
        channel_obj = kwargs.get("channel", None)
        url = kwargs.get("url", discord.Embed.Empty)
        color = kwargs.get("color", discord.Embed.Empty)

        try:
            await channel_obj.send(embed=self.create_embed(embed_title, embed_desc, url, color))
        except discord.Forbidden:
            logging.warning("Bot doesn't have correct permission to for this action")
        except Exception as e:
            logging.warning(e)

    async def send_missing_permission_warning(self, channel):
        embed_title = f"{self.NAME} missing permissions"
        embed_desc = "Bot doesn't have correct permission to for this action"
        logging.warning(embed_desc)
        await self.send_embed(channel=channel, title=embed_title, description=embed_desc, color=self.red_hex_color)

    def check_for_command_identifier(self, message):
        return self.command_identifier == message.content[0]

    def process_bot_embeds(self, message):
        logging.info("We will deal with this latter")
        logging.info(f"{message.embeds[0].title}")
