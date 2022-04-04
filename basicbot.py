import discord
import logging
import datetime
import channelhelper


class MyClient(discord.Client):
    DEFAULT_COMMAND_IDENTIFIER: str = "!"
    command_identifier: str = DEFAULT_COMMAND_IDENTIFIER
    NAME: str = "Trouble Maker"
    PATRON_URL: str = "ConspiratorSoftworks.xyz"
    TIME_START = datetime.datetime.utcnow()
    optional_modules: list = []
    commands_called: int = 0
    bot_embed_title_map: dict = {
        'setup': "Setting up bot configuration"
    }
    red_hex_color: hex = 0xff0000
    green_hex_color: hex = 0x00ff00

    module_map: dict = {
        "voice": channelhelper.ChannelHelper()
    }

    native_commands: list = [
        "setup",
        "info",
        "ping",
        "invite",
        "set"
    ]

    set_params: list = [
        "identifier"
    ]

    async def on_ready(self) -> None:
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, msg: discord.Message) -> None:

        if self.check_if_embed_needs_response(msg):
            await self.process_bot_embeds(msg)

        if not self.check_for_bot_message(msg) and self.check_for_command_identifier(msg):
            function_name = None
            try:
                args = msg.content[1:].lower().split(" ")
                if args[0] in self.module_map:
                    if len(args) < 2:
                        await self.send_improper_command(msg)
                        return
                    function_name = getattr(self.module_map[args[0]], args[1], None)
                else:
                    if args[0] in self.native_commands:
                        function_name = getattr(MyClient, args[0], None)
                if function_name:
                    await function_name(self, msg, args)
                    self.commands_called += 1
            except (AttributeError, TypeError) as e:
                logging.error(e)
            except Exception as e:
                logging.error(e)

    # Native Commands

    async def invite(self, msg: discord.Message, args: list) -> None:
        client_id = self.user.id
        discord_api_url = "https://discord.com/api/oauth2/authorize?client_id="
        invite_url = f"{discord_api_url}{client_id}&permissions=0&scope=bot%20applications.commands"

        embed_title = f"Click here to add {self.NAME} to your server!"
        embed_desc = (f"Thanks for your interest in adding {self.NAME} to your server! "
                      f"Please click the link above to proceed.")

        logging.info(f"User {msg.author.id} has requested a server invite for {self.NAME}")
        await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc, url=invite_url)

    async def ping(self, msg: discord.Message, args: list) -> None:
        await msg.channel.send("Pong!")

    async def info(self, msg: discord.Message, args: list) -> None:
        embed_title = "Bot Info"
        time_diff = datetime.datetime.utcnow() - self.TIME_START
        embed_desc = (f"**Uptime**: {time_diff.days} Days, {time_diff.seconds // 3600} Hours, "
                      f"{time_diff.seconds // 60 % 60} Minutes, {time_diff.seconds % 60} Seconds\n"
                      f"**Servers Found On:** {len(self.guilds)}\n"
                      f"**Commands Run Since Start Up**: {self.commands_called}")
        await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc)

    async def setup(self, msg: discord.Message, args: list) -> None:
        embed_title = self.bot_embed_title_map["setup"]
        embed_desc = (f"First lets select your command identifier\n"
                      f"Run **{self.command_identifier}set identifier <Your chosen identifier>**\n"
                      f"Note: this identifier can't be a number or letter")
        await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc)

    async def set(self, msg: discord.Message, args: list) -> None:
        if len(args) == 1:
            embed_title: str = f"Set Command"
            set_param_str: str = "\n".join(self.set_params)
            embed_desc: str = f"Values that you can set:\n {set_param_str}"
            await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc)
        elif len(args) < 3:
            await self.send_improper_command(msg)
            return
        elif args[1].lower() == "identifier":
            self.command_identifier = args[2]
            embed_title = f"Successfully set new command identifier"
            embed_desc = f"Bot will now use **{self.command_identifier}** to identify commands"
            await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc)
        return

    # Boolean Helpers

    def check_if_embed_needs_response(self, msg: discord.Message) -> bool:
        # Check is message originated from this bot and is in bot_embed_title_map.values()
        return msg.author.id == self.user.id and len(msg.embeds) > 0 and \
               msg.embeds[0].title in self.bot_embed_title_map.values()

    @staticmethod
    def check_for_bot_message(msg: discord.Message) -> bool:
        return msg.author.bot

    def check_for_command_identifier(self, msg: discord.Message) -> bool:
        return self.command_identifier == msg.content[0]

    # Embed related code

    def create_embed(self, title_text: str, desc_text: str, url: str, color_hex: hex) -> discord.Embed:
        if color_hex == discord.Embed.Empty:
            color_hex = self.green_hex_color
        embed_obj = discord.Embed(title=title_text, description=desc_text, color=color_hex, author=self.NAME, url=url,
                                  name=self.user.name, timestamp=datetime.datetime.utcnow())
        embed_obj.set_footer(text=f"Brought to you by {self.PATRON_URL}", icon_url=self.user.avatar_url)
        return embed_obj

    async def send_embed(self, **kwargs) -> None:
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

    async def process_bot_embeds(self, msg: discord.Message) -> None:
        logging.info("We will deal with this latter")
        logging.info(f"{msg.embeds[0].title}")
        if msg.embeds[0].title == self.bot_embed_title_map["setup"]:
            pass

    # Error Handling

    async def send_missing_permission_warning(self, channel: discord.TextChannel) -> None:
        embed_title = f"{self.NAME} missing permissions"
        embed_desc = "Bot doesn't have correct permission to for this action"
        logging.warning(embed_desc)
        await self.send_embed(channel=channel, title=embed_title, description=embed_desc, color=self.red_hex_color)

    async def send_improper_command(self, msg: discord.Message) -> None:
        embed_title = f"Bad command format"
        embed_desc = f"Looks like your command had an issue"
        logging.warning(embed_desc)
        await self.send_embed(channel=msg.channel, title=embed_title, description=embed_desc, color=self.red_hex_color)