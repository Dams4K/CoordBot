import discord

class BotEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_footer(text=str(bot.user) + " | -utip")