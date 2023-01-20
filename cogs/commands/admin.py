import discord
from discord import option
from discord.ext import commands
from discord.ext import bridge
from data_management import MemberData
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="reset")
    @option("member", type=discord.Member, required=True)
    async def reset(self, ctx, member):
        confirm_view = ConfirmView()
        confirm_embed = DangerEmbed(ctx.guild_config, title="ATTENTION")
        confirm_embed.description = f"Êtes-vous sur de vouloir reset {member} ?"

        await ctx.respond(embed=confirm_embed, view=confirm_view)
        await confirm_view.wait()
        
        embed = NormalEmbed(ctx.guild_config, title="Reset")
        if confirm_view.confirmed:
            member_data = MemberData(ctx.guild.id, member.id)
            member_data.reset()
            
            embed.title += " effectué"
            embed.description = f"{member} a été reset"

        else:
            embed.title += " annulé"
            embed.description = f"{member} n'a pas été reset"
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="say")
    async def say(self, ctx, *, message):
        if hasattr(ctx, "message") and ctx.message != None:
            await ctx.message.delete()
        else:
            await ctx.respond("message sent", ephemeral=True)
        await ctx.send(message)


def setup(bot):
    bot.add_cog(AdminCog(bot))