import os, shutil
from discord import *
from data_management import MemberData
from utils.bot_embeds import DangerEmbed, NormalEmbed
from utils.bot_views import ConfirmView
from utils.bot_commands import *
from utils.references import References

class AdminCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    data = BotSlashCommandGroup("data", default_member_permissions=Permissions(administrator=True), guild_only=True, guild_ids=[1061324656075874476])
    server = data.create_subgroup("server")
    member = data.create_subgroup("member")

    @server.command(name="retrieve")
    async def server_retrieve(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_folder = References.get_guild_folder(str(ctx.guild.id))
        zip_path = os.path.join("datas/backups", f"{ctx.guild.id}")

        if os.path.exists(guild_folder):
            shutil.make_archive(zip_path, "zip", guild_folder)
        
        with open(zip_path + ".zip", "rb") as f:
            file = File(f, filename=f"guild_data_{ctx.guild.id}.zip")
            await ctx.respond(file=file)

        os.remove(zip_path + ".zip")

    @server.command(name="reset")
    async def server_reset(self, ctx):
        confirm_view = ConfirmView()
        confirm_embed = DangerEmbed(ctx.guild_config, title=ctx.translate("WARNING"))
        confirm_embed.description = ctx.translate("CLEAR_SERVER_CONFIRMATION", member=member)

        await ctx.respond(embed=confirm_embed, view=confirm_view)
        await confirm_view.wait()
        
        embed = NormalEmbed(ctx.guild_config)
        if confirm_view.confirmed:
            path = References.get_guild_folder(str(ctx.guild.id))
            if os.path.exists(path):
                shutil.rmtree(path)

            embed.title = ctx.translate("CLEAR_DONE")
            embed.description = ctx.translate("SERVER_HAS_BEEN_CLEARED", member=member)

        else:
            embed.title = ctx.translate("CLEAR_CANCELED")
            embed.description = ctx.translate("SERVER_HAS_NOT_BEEN_CLEARED", member=member)
        
        await ctx.respond(embed=embed)

    

    @member.command(name="retrieve")
    @option("member", type=Member)
    async def member_retrieve(self, ctx, member):
        await ctx.defer(ephemeral=True)

        member_data = MemberData(member.id, ctx.guild.id)
        member_data.save()
        with open(member_data._path, "rb") as f:
            file = File(f, filename=f"member_data_{member.id}.json")
            await ctx.respond(file=file)
            

    @member.command(name="reset")
    @default_permissions(administrator=True)
    @option("member", type=Member)
    async def member_reset(self, ctx, member):
        await self.reset_member(ctx, member)    

    @bot_user_command(name="Reset", guild_only=True)
    @default_permissions(administrator=True)
    async def user_reset(self, ctx, member):
        await self.reset_member(ctx, member, ephemeral=True)

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