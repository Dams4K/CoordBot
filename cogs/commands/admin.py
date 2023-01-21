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
        confirm_embed = DangerEmbed(ctx.guild_config, title=await ctx.translate("WARNING"))
        confirm_embed.description = await ctx.translate("RESET_MEMBER_CONFIRMATION", member=member)

        await ctx.respond(embed=confirm_embed, view=confirm_view)
        await confirm_view.wait()
        
        embed = NormalEmbed(ctx.guild_config)
        if confirm_view.confirmed:
            member_data = MemberData(ctx.guild.id, member.id)
            member_data.reset()
            
            embed.title = await ctx.translate("RESET_DONE")
            embed.description = await ctx.translate("MEMBER_HAS_BEEN_RESET", member=member)

        else:
            embed.title = await ctx.translate("RESET_CANCELED")
            embed.description = await ctx.translate("MEMBER_HAS_NOT_BEEN_RESET", member=member)
        
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="say")
    async def say(self, ctx, *, message: str):
        if ctx.is_app:
            await ctx.respond(text_key="MESSAGE_SENT", ephemeral=True)
        else:
            await ctx.message.delete()
        
        await ctx.send(message, text_key="MESSAGE_SENT")


def setup(bot):
    bot.add_cog(AdminCog(bot))