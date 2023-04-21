import discord
import datetime
import shutil
import os
from discord.ext import commands, tasks

class BackupCog(commands.Cog):
    BACKUP_DAYS = [0]
    BACKUP_TIMES = [datetime.time(hour=8, tzinfo=datetime.timezone.utc)]

    def __init__(self, bot):
        self.bot = bot
    
    def cog_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @tasks.loop(time=BACKUP_TIMES)
    async def backup_task(self):
        today = datetime.date.today()
        if today.isoweekday() in [BACKUP_DAYS]:
            await self.create_backup()

    @commands.command(name="force_backup")
    async def force_backup(self, ctx):
        await self.create_backup()
        await ctx.send(self.ctx.translate("NEW_BACKUP_MADE"))


    async def create_backup(self):
        filename = datetime.date.today().strftime("%Y-%m-%d")
        path = f"datas/backups/{filename}"
        
        shutil.make_archive(path, "zip", "datas/guilds")

def setup(bot):
    bot.add_cog(BackupCog(bot))