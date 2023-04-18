import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from lang import Lang
from utils.bot_embeds import NormalEmbed
from utils.references import References
from utils.bot_contexts import BotAutocompleteContext, BotBridgeContext
from data_management import *

class GuildConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return is_admin(ctx)

    async def get_languages(self, ctx: BotAutocompleteContext):
        return [Lang.get_text("CHANGE_LANGUAGE", lang) for lang in Lang.get_languages()]

    async def get_custom_translations(self, ctx):
        guild_language = GuildLanguage(ctx.interaction.guild.id)
        return guild_language.get_keys()


    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("current")
    async def prefix(self, ctx: BotBridgeContext):
        await ctx.respond(f"The bot's prefix is {ctx.guild_config.prefix}")

    @prefix.command(name="set")
    @option("new_prefix", type=str, required=True)
    async def prefix_set(self, ctx, new_prefix: str):
        ctx.guild_config.set_prefix(new_prefix)
        await ctx.respond(text_key="PREFIX_CHANGED", text_args={"prefix": new_prefix})
    
    @prefix.command(name="reset")
    async def prefix_reset(self, ctx):
        ctx.guild_config.set_prefix = References.BOT_PREFIX
        await ctx.respond("The bot's prefix has been reset")


    @bridge.bridge_group()
    async def language(self, ctx):
        pass
    

    @language.command(name="set")
    @option("language", type=str, required=True, autocomplete=get_languages)
    async def set_language(self, ctx, language: str):
        language = language[language.find("(")+1:language.find(")")]
        
        if not Lang.language_is_translated(language):
            await ctx.respond(text_key="NO_TRANSLATION")
        else:
            ctx.guild_config.set_language(language)
            await ctx.respond(text_key="LANGUAGE_CHANGED")


    @language.command(name="override")
    @option("key", type=str, required=True)
    @option("value", type=str, required=True)
    async def override_translation(self, ctx: BotBridgeContext, key, value):
        guild_language = GuildLanguage(ctx.guild.id)
        guild_language.add_translation(key, value)
        await ctx.respond("finish")
    
    @language.command(name="reset")
    @option("key", type=str, required=True, autocomplete=get_custom_translations)
    async def reset_translation(self, ctx, key: str):
        guild_language = GuildLanguage(ctx.guild.id)
        guild_language.reset_translation(key)

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("status")
    @option("enabled", type=bool, required=True)
    async def leveling(self, ctx, enabled: bool):
        leveling_config = GuildLevelingData(ctx.guild.id)
        if enabled:
            leveling_config.enable()
            await ctx.respond(text_key="ENABLE_LEVEL_SYSTEM")
        else:
            leveling_config.disable()
            await ctx.respond(text_key="DISABLE_LEVEL_SYSTEM")

    @leveling.command(name="ban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_ban(self, ctx, member=None, channel=None):
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.ban_member(member)
        leveling_config.ban_channel(channel)

    @leveling.command(name="unban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_unban(self, ctx, member=None, channel=None):
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.unban_member(member)
        leveling_config.unban_channel(channel)

def setup(bot):
    bot.add_cog(GuildConfigCog(bot))