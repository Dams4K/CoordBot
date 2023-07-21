from discord import *

from data_management import *
from lang import Lang
from utils.bot_commands import *
from utils.bot_contexts import BotBridgeContext
from utils.bot_embeds import *
from utils.bot_autocompletes import get_languages, get_translation_keys, get_custom_translations


class GuildConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    language = BotSlashCommandGroup("language", default_member_permissions=Permissions(administrator=True), guild_only=True)

    @language.command(name="change")
    @option("language", type=str, autocomplete=get_languages)
    async def language_change(self, ctx, language: str):
        language = language[language.find("(")+1:language.find(")")]
        
        if not Lang.language_is_translated(language):
            await ctx.respond(text_key="NO_TRANSLATION")
        else:
            ctx.guild_config.set_language(language)
            await ctx.respond(text_key="LANGUAGE_CHANGED")

    @language.command(name="customize")
    @option("key", type=str, required=True, autocomplete=get_translation_keys)
    @option("translation", type=str, required=True)
    async def language_customize(self, ctx: BotBridgeContext, key, translation):
        guild_language = GuildLanguage(ctx.guild.id)
        guild_language.add_translation(key, translation)

        await ctx.respond(text_key="TRANSLATION_HAS_BEEN_MODIFIED", text_args={"key":key})
    
    @language.command(name="reset")
    @option("key", type=str, required=True, autocomplete=get_custom_translations)
    async def language_reset(self, ctx, key: str):
        guild_language = GuildLanguage(ctx.guild.id)
        guild_language.reset_translation(key)

        await ctx.respond(text_key="TRANSLATION_HAS_BEEN_RESET", text_args={"key":key})
    

def setup(bot):
    bot.add_cog(GuildConfigCog(bot))