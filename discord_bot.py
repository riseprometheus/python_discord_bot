import discord
import logging
import datetime
import channelhelper
red_hex_color = 0xff0000


class MyClient(discord.Client):
    COMMAND_IDENTIFIER = "!"
    NAME = "Trouble Maker"
    PATRON_URL = "ConspiratorSoftworks.xyz"
    TIME_START = datetime.datetime.utcnow()
    optional_modules = []
    commands_called = 0
    module_dict = {
        "channel":  True
    }

    async def on_ready(self):
        ch = channelhelper.ChannelHelper()
        self.optional_modules.append(ch)
        logging.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if not self.check_for_bot_message(message) and self.check_for_command_identifier(message):
            try:
                args = message.content[1:].lower().split(" ")

                for module in [MyClient, channelhelper.ChannelHelper]:
                    if module == MyClient:
                        function_name = getattr(module, args[0], None)
                    else:
                        function_name = getattr(module, args[1], None)
                    if function_name:
                        break
                if function_name:
                    await function_name(self, message, args)
                    self.commands_called += 1
            except (AttributeError, TypeError) as e:
                logging.error(e)
                pass
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

    # Helpers

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
        await self.send_embed(channel=channel, title=embed_title, description=embed_desc, color=red_hex_color)

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
