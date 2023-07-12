from discord import *

from data_management import *
from lang import Lang
from utils.bot_commands import *
from utils.bot_contexts import BotAutocompleteContext, BotBridgeContext
from utils.bot_embeds import *


class GuildConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_languages(self, ctx: BotAutocompleteContext):
        return [Lang.get_text("CHANGE_LANGUAGE_TO", lang) for lang in Lang.get_languages()]

    async def get_custom_translations(self, ctx):
        guild_language = GuildLanguage(ctx.interaction.guild.id)
        return guild_language.get_keys()

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
    @option("key", type=str, required=True)
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