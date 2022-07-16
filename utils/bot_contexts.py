import discord
from discord.ext.bridge import BridgeExtContext, BridgeApplicationContext
from utils.data_manager import GuildData, MemberData

class BotApplicationContext(BridgeApplicationContext):
    @property
    def guild_data(self):
        return GuildData(self.guild_id)
    @property
    def author_data(self):
        return MemberData(self.guild_id, self.user.id)

class BotContext(BridgeExtContext):
    @property
    def guild_data(self):
        return GuildData(self.guild.id)
    @property
    def author_data(self):
        return MemberData(self.guild.id, self.author.id)
