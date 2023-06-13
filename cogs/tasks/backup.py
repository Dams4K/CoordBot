import os
import shutil
import datetime

from discord import *
from discord.ext import commands, tasks


class BackupCog(Cog):
    MAX_BACKUPS = 14
    BACKUP_DAYS = [0, 1, 2, 3, 4, 5, 6] # 0 = monday 1 = tuesday 2 = ...
    BACKUP_TIMES = [datetime.time(hour=8)] # utc time

    def __init__(self, bot):
        self.bot = bot
        self.backup_task.start()
    
    def cog_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @tasks.loop(time=BACKUP_TIMES)
    async def backup_task(self):
        today = datetime.date.today()
        if today.weekday() in BACKUP_DAYS:
            backup_path = await self.create_backup()

            app_info = await self.bot.application_info()
            team = app_info.team
            owner: discord.User = await self.bot.fetch_user(team.owner.id) if team else app_info.owner
            if self.send_backup_file(owner, backup_path):
                print(f"Weekly backup file sent to {owner}")


    @commands.command(name="backup")
    async def forced_backup(self, ctx):
        backup_path = await self.create_backup()
        if await self.send_backup_file(ctx.author, backup_path):
            print(f"Forced backup file sent to {ctx.author}")


    async def create_backup(self):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"datas/backups/{filename}"
        
        shutil.make_archive(path, "zip", "datas/guilds")

        backups = os.listdir(f"datas/backups")
        backups.sort()
        while len(backups) > self.MAX_BACKUPS:
            path = backups[0]
            os.remove(path)
            print(f"backup file {path} has been removed")

        return f"{path}.zip"


    async def send_backup_file(self, user, backup_path):
        if not user.can_send():
            return False

        with open(backup_path, "rb") as f:
            file = File(f, backup_path.split("/")[-1])
            await user.send(file=file)
        return True
        

def setup(bot):
    bot.add_cog(BackupCog(bot))