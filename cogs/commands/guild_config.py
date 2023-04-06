import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import is_admin
from lang import Lang
from utils.bot_embeds import NormalEmbed
from utils.references import References
from utils.bot_contexts import BotAutocompleteContext, BotBridgeContext
from data_management import GuildLanguage, DefaultMemberData

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


    @commands.Cog.listener()
    async def on_application_command_auto_complete(self, interaction, command):
        pass

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

    @bridge.bridge_group()
    async def level_system(self, ctx):
        pass

    @level_system.command(name="enabled")
    async def activate(self, ctx, activated: bool):
        ctx.guild_config.enable_level_system(activated)
        await ctx.respond(text_key="ENABLE_LEVEL_SYSTEM" if activated else "DISABLE_LEVEL_SYSTEM")


    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("show")
    async def default_member(self, ctx):
        default_member = DefaultMemberData(ctx.guild.id)
        embed = NormalEmbed(ctx.guild_config, title="Default Member")

        embed.add_field(name="Level", value=default_member.level)
        embed.add_field(name="XP", value=default_member.xp)
        embed.add_field(name="Money", value=default_member.money)

        await ctx.respond(embed=embed)

    @default_member.command(name="setlevel")
    @option("level", type=int, required=True)
    async def dm_set_level(self, ctx, level):
        default_member = DefaultMemberData(ctx.guild.id)
        default_member.set_level(level)

def setup(bot):
    bot.add_cog(GuildConfigCog(bot))