import discord

class BotEmbed(discord.Embed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(**kwargs)
        if guild_config is not None:
            prefix = guild_config.prefix
            self.set_footer(text=f"{prefix}utip")

class NormalEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_green()

class WarningEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.orange()

class DangerEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_red()

class InformativeEmbed(BotEmbed):
    def __init__(self, guild_config, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.blurple()