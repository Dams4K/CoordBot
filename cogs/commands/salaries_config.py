from discord import *

from data_management import GuildSalaries
from utils.bot_commands import BotSlashCommandGroup
from utils.bot_embeds import DangerEmbed, NormalEmbed


class SalariesConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    salaries = BotSlashCommandGroup("salaries", default_member_permissions=Permissions(administrator=True), guild_only=True)

    @salaries.command(name="add")
    @option("role", type=Role, required=True)
    @option("pay", type=int, required=True)
    async def salaries_add(self, ctx, role: Role, pay: int):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.add_salary(role, pay)

        embed = NormalEmbed(
            title=ctx.translate("ROLE_ADDED"),
            description=ctx.translate("SALARY_ROLE_ADDED", role=role.mention))

        await ctx.respond(embed=embed)
    
    @salaries.command(name="remove")
    @option("role", type=Role, required=True)
    async def salaries_remove(self, ctx, role: Role):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.remove_salary(role)
        
        embed = DangerEmbed(
            title=ctx.translate("ROLE_REMOVED"),
            description=ctx.translate("SALARY_ROLE_REMOVED", role=role.mention))

        await ctx.respond(embed=embed)

    @salaries.command(name="forced_pay")
    @option("member", type=Member, required=False)
    @option("role", type=Role, required=False)
    async def salaries_forced_pay(self, ctx, member: Member = None, role: Role = None):
        guild_salaries = GuildSalaries(ctx.guild.id)

        embed = NormalEmbed(title=ctx.translate("SALARY_FORCED_PAY"))
        if guild_salaries.pay_member(member):
            embed.description = ctx.translate("SALARY_MEMBER_FORCED_PAY", member=member)
        if guild_salaries.pay_role(role):
            embed.add_field(name=ctx.translate("SALARY_ROLE_FORCED_PAY"), value="\n".join([member.mention for member in role.members]))

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(SalariesConfigCog(bot))