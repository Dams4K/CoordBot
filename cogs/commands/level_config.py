from discord import *
from discord.ext.pages import Paginator

from data_management import *
from utils.bot_commands import BotSlashCommandGroup
from utils.bot_embeds import *


class LevelConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    experience = BotSlashCommandGroup("experience", default_member_permissions=Permissions(administrator=True), guild_only=True)
    level = BotSlashCommandGroup("level", default_member_permissions=Permissions(administrator=True), guild_only=True)
    leveling = BotSlashCommandGroup("leveling", default_member_permissions=Permissions(administrator=True), guild_only=True)
    banlist = leveling.create_subgroup("banlist")
    set = leveling.create_subgroup("set")

    @experience.command(name="add")
    @option("to", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(amount)
        await ctx.respond(text_key="XP_ADDED", text_args={"amount": amount, "member": member})
        

    @experience.command(name="remove")
    @option("to", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(-amount)
        await ctx.respond(text_key="XP_REMOVED", text_args={"amount": amount, "member": member})
    

    @experience.command(name="set")
    @option("for", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_xp(amount)
        await ctx.respond(text_key="XP_SET", text_args={"amount": amount, "member": member})


    @level.command(name="add")
    @option("to", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(amount)
        await ctx.respond(text_key="LEVEL_ADDED", text_args={"amount": amount, "member": member})
        

    @level.command(name="remove")
    @option("to", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(-amount)
        await ctx.respond(text_key="LEVEL_REMOVED", text_args={"amount": amount, "member": member})
    

    @level.command(name="set")
    @option("for", parameter_name="member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_level(amount)
        await ctx.respond(text_key="LEVEL_SET", text_args={"amount": amount, "member": member})


    @leveling.command(name="enable")
    async def leveling_enable(self, ctx):
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.enable()

        embed = NormalEmbed(title=ctx.translate("ACTIVATION"), description=ctx.translate("ENABLE_LEVELING"))
        await ctx.respond(embed=embed)


    @leveling.command(name="disable")
    async def leveling_disable(self, ctx):
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.disable()

        embed = DangerEmbed(title=ctx.translate("DEACTIVATION"), description=ctx.translate("DISABLE_LEVELING"))
        await ctx.respond(embed=embed)

    @leveling.command(name="status")
    async def leveling_status(self, ctx):
        leveling_config = GuildLevelingConfig(ctx.guild.id)

        embed = InformativeEmbed(title=ctx.translate("LEVELING_STATUS"))
        embed.description = ctx.translate("LEVELING_CURRENTLY_ENABLED") if leveling_config.enabled else ctx.translate("LEVELING_CURRENTLY_DISABLED")

        embed.add_field(name=ctx.translate("LEVELING_MESSAGE"), value=leveling_config.level_up_message, inline=False)
        embed.add_field(name=ctx.translate("LEVELING_GAIN_RANGE"), value=ctx.translate("LEVELING_GAIN_RANGE_TEXT", min=leveling_config.min_gain, max=leveling_config.max_gain), inline=False)
        embed.add_field(name=ctx.translate("LEVELING_FORMULA"), value=leveling_config.formula, inline=False)
        await ctx.respond(embed=embed)

    @leveling.command(name="ban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_ban(self, ctx, member=None, channel=None):
        if member is None and channel is None:
            embed = WarningEmbed(title=ctx.translate("WARNING"), description=ctx.translate("NOTHING_SELECTED"))
            await ctx.respond(embed=embed)
            return

        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.ban_member(member)
        leveling_config.ban_channel(channel)

        description = []
        if not member is None:
            description.append(ctx.translate("LEVELING_MEMBER_HAS_BEEN_BANNED", member=member))
        if not channel is None:
            description.append(ctx.translate("LEVELING_CHANNEL_HAS_BEEN_BANNED", channel=channel.mention))

        embed = NormalEmbed(title=ctx.translate("BANNING"), description="\n".join(description))
        await ctx.respond(embed=embed)

    @leveling.command(name="unban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_unban(self, ctx, member=None, channel=None):
        if member is None and channel is None:
            embed = WarningEmbed(title=ctx.translate("WARNING"), description=ctx.translate("NOTHING_SELECTED"))
            await ctx.respond(embed=embed)
            return
        
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.unban_member(member)
        leveling_config.unban_channel(channel)

        description = []
        if not member is None:
            description.append(ctx.translate("LEVELING_MEMBER_HAS_BEEN_UNBANNED", member=member))
        if not channel is None:
            description.append(ctx.translate("LEVELING_CHANNEL_HAS_BEEN_UNBANNED", channel=channel.mention))

        embed = DangerEmbed(title=ctx.translate("UNBANNING"), description="\n".join(description))
        await ctx.respond(embed=embed)

    @banlist.command(name="members")
    async def banlist_members(self, ctx):
        title = ctx.translate("LEVELING_BANLIST_MEMBERS")

        members = [ctx.guild.get_member(member_id) for member_id in GuildLevelingConfig(ctx.guild.id).banned_members]
        embeds = [NormalEmbed(title=title, description="\n".join([member.mention for member in members[i:i+20] if member is not None])) for i in range(0, len(members), 20)]
        
        if embeds == []:
            await ctx.respond(embed=NormalEmbed(title=title, description=ctx.translate("LEVELING_BANLIST_MEMBERS_EMPTY")))
        else:
            paginator = Paginator(pages=embeds, show_disabled=False)
            await paginator.respond(ctx.interaction)

    @banlist.command(name="channels")
    async def banlist_channels(self, ctx):
        title = ctx.translate("LEVELING_BANLIST_CHANNELS")

        channels = [ctx.guild.get_channel_or_thread(channel_id) for channel_id in GuildLevelingConfig(ctx.guild.id).banned_channels]
        embeds = [NormalEmbed(title=title, description="\n".join([channel.mention for channel in channels[i:i+20] if channel is not None])) for i in range(0, len(channels), 20)]
    
        if embeds == []:
            await ctx.respond(embed=NormalEmbed(title=title, description=ctx.translate("LEVELING_BANLIST_CHANNELS_EMPTY")))
        else:
            paginator = Paginator(pages=embeds, show_disabled=False)
            await paginator.respond(ctx.interaction)

    @set.command(name="gain")
    @option("min", type=int)
    @option("max", type=int)
    async def set_gain(self, ctx, min: int, max: int):
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.set_min_gain(min)
        leveling_config.set_max_gain(max)

        await ctx.respond(text_key="GAIN_RANGE_MODIFIED", text_args={"min": min, "max": max})
    
    @set.command(name="message")
    @option("message", type=str, max_length=512)
    async def set_message(self, ctx, message: str):
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        leveling_config.set_message(message)

        await ctx.respond(text_key="LEVEL_UP_MESSAGE_MODIFIED")


def setup(bot):
    bot.add_cog(LevelConfigCog(bot))