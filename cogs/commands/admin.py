import os, shutil
from discord import *
from data_management import MemberData
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView
from utils.permissions import is_admin
from utils.bot_commands import *
from utils.references import References

class AdminCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    data = BotSlashCommandGroup("data")

    @data.command(name="retrieve")
    async def data_retrieve(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_folder = References.get_guild_folder(str(ctx.guild.id))
        zip_path = os.path.join(guild_folder, f"{ctx.guild.id}")

        if os.path.exists(guild_folder):
            shutil.make_archive(zip_path, "zip", guild_folder)
        
        with open(zip_path + ".zip", "r") as f:
            file = File(f)
            await ctx.respond(file=file)

        os.remove(zip_path + ".zip")

    def delete_guild_folder(self, guild_id):
        path = References.get_guild_folder(str(guild_id))
        return path

    @bot_user_command(name="reset")
    @default_permissions(administrator=True)
    async def user_reset(self, ctx, member):
        await self.reset_member(ctx, member, ephemeral=True)

    @bot_slash_command(name="reset")
    @default_permissions(administrator=True)
    @option("member", type=Member)
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