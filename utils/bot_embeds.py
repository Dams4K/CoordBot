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
    texts   =   [ "go outside", "have you heard about CPS Display?",    "play minecraft.",    None,   '*watch "person of interest"',    "Tunic is a masterpiece",   "FMA is a masterpiece too!",    "good bye.",   "as your wish",  "secrets are everywhere",   "[ Fourth wall is shaking ]" ]
    weights =   [ 10,           3,                                      4,                    30,     3,                                3,                          3,                              15,             15,             9,                          6 ]
    
    return choices(texts, weights=weights)[0] 