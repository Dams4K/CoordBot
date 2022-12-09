import discord

class BotEmbed(discord.Embed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(**kwargs)
        prefix = guild_config.prefix
        self.set_footer(text=f"{prefix}utip")

class NormalEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_green()

class DangerEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_red()