import discord
from discord import option
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import *
from utils.bot_contexts import MemberData

class LevelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @bridge.bridge_group(name="xp", checks=[is_admin])
    async def xp_group(self, ctx): pass

    @xp_group.command(name="add")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def add_xp(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_xp(amount)
        await ctx.respond(text_key="XP_ADDED", text_args={"amount": amount, "member": member})
        

    @xp_group.command(name="remove")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def remove_xp(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.add_xp(-amount)
        await ctx.respond(text_key="XP_REMOVED", text_args={"amount": amount, "member": member})
    

    @xp_group.command(name="set")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def set_xp(self, ctx, member, amount):
        member_data = MemberData(ctx.guild.id, member.id)
        member_data.set_xp(amount)
        await ctx.respond(text_key="XP_SET", text_args={"amount": amount, "member": member})


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        member_data = MemberData(message.guild.id, message.author.id)
        member_data.add_xp(len(message.content))


def setup(bot):
    bot.add_cog(LevelsCog(bot))