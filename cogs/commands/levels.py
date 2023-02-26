import discord
from discord import option
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from utils.permissions import *
from utils.bot_contexts import MemberData
from utils.bot_embeds import NormalEmbed
from operator import attrgetter

class LevelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @bridge.bridge_group(checks=[is_admin])
    async def xp(self, ctx): pass

    @xp.command(name="add")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(amount)
        await ctx.respond(text_key="XP_ADDED", text_args={"amount": amount, "member": member})
        

    @xp.command(name="remove")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(-amount)
        await ctx.respond(text_key="XP_REMOVED", text_args={"amount": amount, "member": member})
    

    @xp.command(name="set")
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_xp(amount)
        await ctx.respond(text_key="XP_SET", text_args={"amount": amount, "member": member})


    @bridge.bridge_group()
    async def level(self, ctx): pass

    @level.command(name="add", checks=[is_admin])
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def level_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(amount)
        await ctx.respond(text_key="LEVEL_ADDED", text_args={"amount": amount, "member": member})
        

    @level.command(name="remove", checks=[is_admin])
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def level_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(-amount)
        await ctx.respond(text_key="LEVEL_REMOVED", text_args={"amount": amount, "member": member})
    

    @level.command(name="set", checks=[is_admin])
    @option("member", type=discord.Member, required=True)
    @option("amount", type=int, required=True)
    async def level_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_level(amount)
        await ctx.respond(text_key="LEVEL_SET", text_args={"amount": amount, "member": member})

    @level.command(name="top")
    async def level_top(self, ctx):
        members_data = [MemberData(member.id, ctx.guild.id) for member in ctx.guild.members]
        members_data.sort(key=attrgetter("level", "xp"), reverse=True)
        
        formatted_top = []
        for i in range(0, min(15, len(members_data))):
            member_data = members_data[i]
            member = discord.utils.find(lambda m: m.id == member_data._member_id, ctx.guild.members)
            formatted_top.append(f"{i+1}. {member.name if member is not None else None}: {member_data.level}")

        embed = NormalEmbed(ctx.guild_config, title="Top 15 levels")
        embed.description = "\n".join(formatted_top)
        await ctx.respond(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ctx = await self.bot.get_context(message)

        if not ctx.command is None or not ctx.guild_config.level_system_enabled:
            return

        level_before = ctx.author_data.level
        ctx.author_data.add_xp(len(message.content))
        level_after = ctx.author_data.refresh_level(ctx.guild_config.leveling_formula)

        if level_before < level_after:
            await ctx.send(ctx.guild_config.send_level_up_message(ctx.author, level_before, level_after))


def setup(bot):
    bot.add_cog(LevelsCog(bot))