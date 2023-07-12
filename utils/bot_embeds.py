import discord
from random import choices

class BotEmbed(discord.Embed):
    def __init__(self, guild_config = None, **kwargs):
        super().__init__(**kwargs)
        if guild_config is not None:
            prefix = guild_config.prefix
        
        if text := get_text_footer():
            self.set_footer(text=text)

class NormalEmbed(BotEmbed):
    def __init__(self, guild_config = None, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_green()

class WarningEmbed(BotEmbed):
    def __init__(self, guild_config = None, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.orange()

class DangerEmbed(BotEmbed):
    def __init__(self, guild_config = None, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.brand_red()

class InformativeEmbed(BotEmbed):
    def __init__(self, guild_config = None, **kwargs):
        super().__init__(guild_config, **kwargs)
        self.color = discord.Colour.blurple()

def get_text_footer():
    texts = {
        None: 180,
        "go outside": 10,
        "have you heard about CPS Display?": 3,
        "play minecraft.": 4,
        '*watch "person of interest"': 3,
        "FMA is a masterpiece too!": 3,
        "Tunic is a masterpiece": 4,
        "good bye.": 15,
        "as you wish": 15,
        "secrets are everywhere": 4,
        "[ Fourth wall is shaking ]": 6
    }
    r = choices(list(texts.keys()), weights=list(texts.values()))
    print(r)
    return r[0] 