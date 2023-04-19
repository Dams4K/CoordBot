from discord import *
from data_management import MemberData
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView
from utils.permissions import is_admin
from lang import get_command_args

class AdminCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @user_command(**get_command_args("reset"))
    @default_permissions(administrator=True)
    async def user_reset(self, ctx, member):
        await self.reset_member(ctx, member, ephemeral=True)

    @slash_command(**get_command_args("reset"))
    @default_permissions(administrator=True)
    @option(
        "member", type=Member, required=True,
        description="Member to reset",
        name_localizations={
            "fr": "membre"
        },
        description_localizations={
            "fr": "Membre à réinitialiser"
        },
    )
    async def slash_reset(self, ctx, member):
        await self.reset_member(ctx, member)

    async def reset_member(self, ctx, member: Member, ephemeral=False):
        confirm_view = ConfirmView()
        confirm_embed = DangerEmbed(ctx.guild_config, title=ctx.translate("WARNING"))
        confirm_embed.description = ctx.translate("RESET_MEMBER_CONFIRMATION", member=member)

        await ctx.respond(embed=confirm_embed, view=confirm_view, ephemeral=ephemeral)
        await confirm_view.wait()
        
        embed = NormalEmbed(ctx.guild_config)
        if confirm_view.confirmed:
            member_data = MemberData(member.id, ctx.guild.id)
            member_data.delete()
            
            embed.title = ctx.translate("RESET_DONE")
            embed.description = ctx.translate("MEMBER_HAS_BEEN_RESET", member=member)

        else:
            embed.title = ctx.translate("RESET_CANCELED")
            embed.description = ctx.translate("MEMBER_HAS_NOT_BEEN_RESET", member=member)
        
        await ctx.respond(embed=embed, ephemeral=ephemeral)

def setup(bot):
    bot.add_cog(AdminCog(bot))