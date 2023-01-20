import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from lang import Lang

class GuildConfigCog(commands.Cog):
    LANGUAGES = [
        "en",
        "fr"
    ]

    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    async def get_languages(self, ctx: discord.AutocompleteContext):
        return [Lang.get_text("CHANGE_LANGUAGE", lang) for lang in self.LANGUAGES]

    @bridge.bridge_command(name="setprefix")
    @option("prefix", type=str, required=True)
    async def set_prefix(self, ctx, prefix: str):
        ctx.guild_config.set_prefix(prefix)
        await ctx.respond("Prefix changed to " + prefix)
    

    @bridge.bridge_command(name="set_lang")
    @option("new_language", type=str, required=True, autocomplete=get_languages)
    async def set_lang(self, ctx, new_language: str):
        new_language = new_language[new_language.find("(")+1:new_language.find(")")]
        ctx.guild_config.set_language(new_language)
        await ctx.respond(ctx.translate("LANGUAGE_CHANGED"))


def setup(bot):
    bot.add_cog(GuildConfigCog(bot))