from discord import *
from data_management import GuildSalaries

class SalariesConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    salary = SlashCommandGroup("salary", default_member_permissions=Permissions(administrator=True))

    @salary.command(name="add")
    @option("role", type=Role, required=True)
    @option("pay", type=int, required=True)
    async def salary_add(self, ctx, role: Role, pay: int):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.add_salary(role, pay)
    
    @salary.command(name="remove")
    @option("role", type=Role, required=True)
    async def salary_remove(self, ctx, role: Role):
        salaries = GuildSalaries(ctx.guild.id)
        salaries.remove_salary(role)

    @salary.command(name="pay")
    @option("member", type=Member, required=False)
    @option("role", type=Role, required=False)
    async def salary_pay(self, ctx, member: Member, role: Role):
        pass

def setup(bot):
    bot.add_cog(SalariesConfigCog(bot))