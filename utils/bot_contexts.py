import discord
from discord.commands.context import ApplicationContext
from discord.ext.commands.context import Context
from utils.data_manager import GuildData, MemberData

class BotApplicationContext(ApplicationContext):
    @property
    def guild_data(self):
        return GuildData(self.guild_id)
    @property
    def member_data(self):
        return MemberData(self.guild_id, self.user.id)

class BotContext(Context):
    @property
    def guild_data(self):
        return GuildData(self.guild.id)
    @property
    def member_data(self):
        return MemberData(self.guild.id, self.author.id)