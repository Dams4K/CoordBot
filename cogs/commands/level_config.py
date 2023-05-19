from discord import *
from discord.ext.pages import Paginator
from utils.permissions import *
from utils.bot_embeds import *
from utils.bot_commands import BotSlashCommandGroup
from data_management import *

class LevelConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    experience = BotSlashCommandGroup("experience", default_member_permissions=Permissions(administrator=True), guild_only=True)
    level = BotSlashCommandGroup("level", default_member_permissions=Permissions(administrator=True), guild_only=True)
    leveling = BotSlashCommandGroup("leveling", default_member_permissions=Permissions(administrator=True), guild_only=True)
    banlist = leveling.create_subgroup("banlist")
    l_set = leveling.create_subgroup("set")

    @experience.command(name="add")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(amount)
        await ctx.respond(text_key="XP_ADDED", text_args={"amount": amount, "member": member})
        

    @experience.command(name="remove")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_xp(-amount)
        await ctx.respond(text_key="XP_REMOVED", text_args={"amount": amount, "member": member})
    

    @experience.command(name="set")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def xp_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_xp(amount)
        await ctx.respond(text_key="XP_SET", text_args={"amount": amount, "member": member})


    @level.command(name="add")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_add(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(amount)
        await ctx.respond(text_key="LEVEL_ADDED", text_args={"amount": amount, "member": member})
        

    @level.command(name="remove")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_remove(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.add_level(-amount)
        await ctx.respond(text_key="LEVEL_REMOVED", text_args={"amount": amount, "member": member})
    

    @level.command(name="set")
    @option("member", type=Member, required=True)
    @option("amount", type=int, required=True)
    async def level_set(self, ctx, member, amount):
        member_data = MemberData(member.id, ctx.guild.id)
        member_data.set_level(amount)
        await ctx.respond(text_key="LEVEL_SET", text_args={"amount": amount, "member": member})


    @leveling.command(name="enable")
    async def leveling_enable(self, ctx):
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.enable()

        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("ACTIVATION"), description=ctx.translate("ENABLE_LEVELING"))
        await ctx.respond(embed=embed)


    @leveling.command(name="disable")
    async def leveling_disable(self, ctx):
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.disable()

        embed = DangerEmbed(ctx.guild_config, title=ctx.translate("DEACTIVATION"), description=ctx.translate("DISABLE_LEVELING"))
        await ctx.respond(embed=embed)


    @leveling.command(name="ban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_ban(self, ctx, member=None, channel=None):
        if member is None and channel is None:
            embed = WarningEmbed(ctx.guild_config, title=ctx.translate("WARNING"), description=ctx.translate("NOTHING_SELECTED"))
            await ctx.respond(embed=embed)
            return

        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.ban_member(member)
        leveling_config.ban_channel(channel)

        description = []
        if not member is None:
            description.append(ctx.translate("LEVELING_MEMBER_BANNED", member=member.mention))
        if not channel is None:
            description.append(ctx.translate("LEVELING_CHANNEL_BANNED", channel=channel.mention))

        embed = NormalEmbed(ctx.guild_config, title=ctx.translate("BAN"), description="\n".join(description))
        await ctx.respond(embed=embed)

    @leveling.command(name="unban")
    @option("member", type=discord.Member, require=False, default=None)
    @option("channel", type=discord.TextChannel, required=False, default=None)
    async def leveling_unban(self, ctx, member=None, channel=None):
        if member is None and channel is None:
            embed = WarningEmbed(ctx.guild_config, title=ctx.translate("WARNING"), description=ctx.translate("NOTHING_SELECTED"))
            await ctx.respond(embed=embed)
            return
        
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.unban_member(member)
        leveling_config.unban_channel(channel)

        description = []
        if not member is None:
            description.append(ctx.translate("LEVELING_MEMBER_UNBANNED", member=member.mention))
        if not channel is None:
            description.append(ctx.translate("LEVELING_CHANNEL_UNBANNED", channel=channel.mention))

        embed = DangerEmbed(ctx.guild_config, title=ctx.translate("UNBAN"), description="\n".join(description))
        await ctx.respond(embed=embed)

    @banlist.command(name="members")
    async def banlist_members(self, ctx):
        members = [ctx.guild.get_member(member_id) for member_id in GuildLevelingData(ctx.guild.id).members_banned]
        embeds = [NormalEmbed(ctx.guild_config, title=ctx.translate("LEVELING_BANLIST_MEMBERS"), description="\n".join([member.mention for member in members[i:i+20] if member is not None])) for i in range(0, len(members), 20)]

        paginator = Paginator(pages=embeds)
        await paginator.respond(ctx.interaction)

    @banlist.command(name="channels")
    async def banlist_channels(self, ctx):
        channels = [ctx.guild.get_channel_or_thread(channel_id) for channel_id in GuildLevelingData(ctx.guild.id).channels_banned]
        embeds = [NormalEmbed(ctx.guild_config, title=ctx.translate("LEVELING_BANLIST_CHANNELS"), description="\n".join([channel.mention for channel in channels[i:i+20] if channel is not None])) for i in range(0, len(channels), 20)]

        paginator = Paginator(pages=embeds)
        await paginator.respond(ctx.interaction)

    @l_set.command(name="gain")
    @option("min", type=int)
    @option("max", type=int)
    async def set_gain(self, ctx, min: int, max: int):
        leveling_config = GuildLevelingData(ctx.guild.id)
        leveling_config.set_min_gain(min)
        leveling_config.set_max_gain(max)

        title = ctx.translate("GAIN_RANGE_MODIFIED")
        description = ctx.translate("GAIN_RANGE_MODIFIED_DESC", min=min, max=max)
        embed = NormalEmbed(ctx.guild_config, title=title, description=descriptions)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(LevelConfigCog(bot))