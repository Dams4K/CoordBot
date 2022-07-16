import discord

class BotEmbed(discord.Embed):
    def __init__(self, title, **kwargs):
        super().__init__(title=title, **kwargs)
        self.set_footer(text="qsd https://www.youtube.com")

embed = BotEmbed("qsd")