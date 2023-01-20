import discord
from discord.ext.bridge import BridgeExtContext, BridgeApplicationContext
from data_management import GuildConfig, MemberData
from lang import Lang

class BotApplicationContext(BridgeApplicationContext):
    @property
    def guild_config(self):
        return GuildConfig(self.guild_id)
    @property
    def author_data(self):
        return MemberData(self.guild_id, self.user.id)
    
    def translate(self, text_key: str, **options):
        return Lang.get_text(text_key, self.guild_config.language, **options)

class BotContext(BridgeExtContext):
    @property
    def guild_config(self):
        return GuildConfig(self.guild.id)
    @property
    def author_data(self):
        return MemberData(self.guild.id, self.author.id)
