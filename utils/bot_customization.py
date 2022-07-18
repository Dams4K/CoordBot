import discord

class BotEmbed(discord.Embed):
    def __init__(self, ctx, **kwargs):
        super().__init__(**kwargs)
        prefix = ctx.guild_data.get_prefix()
        self.set_footer(text=f"{prefix}utip")