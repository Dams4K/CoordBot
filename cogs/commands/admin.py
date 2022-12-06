import discord
from discord.ext import commands
from discord.ext import bridge
from data_management import MemberData
from utils.bot_customization import BotEmbed

class AdminCog(commands.Cog):
    LANGS = [
        "en",
        "fr"
    ]

    def __init__(self, bot):
        self.bot = bot


    async def get_langs(self, ctx: discord.AutocompleteContext):
        return self.LANGS


    @commands.slash_command(name="reset")
    async def slash_reset(self, ctx, member: discord.Option(discord.Member, "member", required=True)):
        await ctx.respond(**await self.reset(ctx, member))

    @commands.command(name="reset")
    async def cmd_reset(self, ctx, member: discord.Member):
        await ctx.send(**await self.reset(ctx, member))

    async def reset(self, ctx, member):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.reset()
        
        embed = BotEmbed(ctx, title="Reset")
        embed.description = f"{member} a été reset"
        return {"embed": embed}

    @bridge.bridge_command(name="say")
    async def say(self, ctx, *, message):
        if hasattr(ctx, "message") and ctx.message != None:
            await ctx.message.delete()
        await ctx.send(message)

    @bridge.bridge_command(name="set_lang")
    async def set_lang(self, ctx, lang: discord.Option(str, "lang", required=True, autocomplete=get_langs)):
        pass
    



def setup(bot):
    bot.add_cog(AdminCog(bot))