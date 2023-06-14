from operator import attrgetter

from discord import *
from discord.ext import commands, pages

from data_management import *
from utils.bot_autocompletes import *
from utils.bot_commands import *
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView


class StorageCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    
    

def setup(bot):
    bot.add_cog(StorageCog(bot))