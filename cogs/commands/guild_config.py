import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from lang import Lang

class GuildConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    async def get_languages(self, ctx: discord.AutocompleteContext):
        return [Lang.get_text("CHANGE_LANGUAGE", lang) for lang in Lang.get_languages()]

    @bridge.bridge_command(name="setprefix")
    @option("prefix", type=str, required=True)
    async def set_prefix(self, ctx, prefix: str):
        ctx.guild_config.set_prefix(prefix)

        await ctx.respond(text_key="PREFIX_CHANGED", text_args={"prefix": prefix})
    

    @bridge.bridge_command(name="setlang")
    @option("lang", type=str, required=True, autocomplete=get_languages)
    async def set_lang(self, ctx, lang: str):
        lang = lang[lang.find("(")+1:lang.find(")")]
        
        if not Lang.language_is_translated(lang):
            await ctx.respond(text_key="NO_TRANSLATION")
            return

        ctx.guild_config.set_language(lang)
        await ctx.respond(text_key="LANGUAGE_CHANGED")


def setup(bot):
    bot.add_cog(GuildConfigCog(bot))