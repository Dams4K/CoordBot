from discord import *
from discord.ext import bridge
from lang import Lang
from utils.permissions import is_in_guild
from utils.bot_embeds import *
from utils.references import References
from utils.bot_contexts import BotAutocompleteContext, BotBridgeContext
from utils.bot_commands import *
from data_management import *

class GuildConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_languages(self, ctx: BotAutocompleteContext):
        return [Lang.get_text("CHANGE_LANGUAGE_TO", lang) for lang in Lang.get_languages()]

    async def get_custom_translations(self, ctx):
        guild_language = GuildLanguage(ctx.interaction.guild.id)
        return guild_language.get_keys()

    @bridge.bridge_group(invoke_without_command=True, checks=[is_in_guild], guild_only=True)
    @bridge.map_to("current")
    async def prefix(self, ctx: BotBridgeContext):
        await ctx.respond(text_key="PREFIX_CURRENT", text_args={"prefix": ctx.guild_config.prefix})

    @prefix.command(name="set")
    @option("new_prefix", type=str, required=True)
    async def prefix_set(self, ctx, new_prefix: str):
        ctx.guild_config.set_prefix(new_prefix)
        await ctx.respond(text_key="PREFIX_CHANGED", text_args={"prefix": new_prefix})
    
    @prefix.command(name="reset")
    async def prefix_reset(self, ctx):
        ctx.guild_config.set_prefix = References.BOT_PREFIX
        await ctx.respond(text_key="PREFIX_CHANGED", text_args={"prefix": References.BOT_PREFIX})

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

        embed = DangerEmbed(title=ctx.translate("TRANSLATION_HAS_BEEN_RESET"), description=ctx.translate("TRANSLATION_HAS_BEEN_RESET_DESC"))

        await ctx.respond(embed=embed)
    

def setup(bot):
    bot.add_cog(GuildConfigCog(bot))