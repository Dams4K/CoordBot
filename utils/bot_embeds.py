import discord

class BotEmbed(discord.Embed):
    def __init__(self, ctx, **kwargs):
        super().__init__(**kwargs)
        prefix = ctx.guild_config.prefix
        self.set_footer(text=f"{prefix}utip")

class NormalEmbed(BotEmbed):
    def __init__(self, ctx, **kwargs):
        super().__init__(ctx, **kwargs)
        self.color = discord.Colour.brand_green()

class DangerEmbed(BotEmbed):
    def __init__(self, ctx, **kwargs):
        super().__init__(ctx, **kwargs)
        self.color = discord.Colour.brand_red()