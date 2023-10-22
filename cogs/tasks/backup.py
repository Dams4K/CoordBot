import datetime
import os
import shutil

from time import time

from discord import *
from discord.ext import commands, tasks


class BackupCog(Cog):
    BACKUPS_FOLDER = "datas/backups"
    MAX_BACKUPS = 14
    BACKUP_DAYS = [0, 1, 2, 3, 4, 5, 6] # 0 = monday; 1 = tuesday; 2 = ...
    BACKUP_TIMES = [datetime.time(hour=8)] # utc time

    def __init__(self, bot):
        self.bot = bot
        self.backup_task.start()
        self.remove_dead_guilds_data()
    
    def cog_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @tasks.loop(time=BACKUP_TIMES)
    async def backup_task(self):
        today = datetime.date.today()
        if today.weekday() in self.BACKUP_DAYS:
            backup_path = await self.create_backup()

            app_info = await self.bot.application_info()
            team = app_info.team
            owner: User = await self.bot.fetch_user(team.owner.id) if team else app_info.owner
            if await self.send_backup_file(owner, backup_path):
                self.bot.logger.info(f"Weekly backup file sent to {owner}")


    @commands.command(name="backup")
    async def forced_backup(self, ctx):
        backup_path = await self.create_backup()
        if await self.send_backup_file(ctx.author, backup_path):
            self.bot.logger.info(f"Forced backup sent to {ctx.author}")


    async def create_backup(self):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.BACKUPS_FOLDER, filename)

        self.remove_dead_guilds_data()
        shutil.make_archive(path, "zip", "datas/guilds")

        backups = os.listdir(self.BACKUPS_FOLDER)
        backups.sort()
        # Delete excess backups 
        while len(backups) > self.MAX_BACKUPS:
            backup_path = os.path.join(self.BACKUPS_FOLDER, backups.pop(0))
            os.remove(backup_path)
            self.bot.logger.info(f"Backup file {backup_path} has been removed")

        return f"{path}.zip"


    async def send_backup_file(self, user, backup_path) -> bool:
        try:
            with open(backup_path, "rb") as f:
                file = File(f, backup_path.split("/")[-1])
                await user.send(file=file)
                return True
        except errors.Forbidden as e:
            self.bot.logger.error(f"Can't send backup file to {user.display_name}: {e}")
        
        return False
    
    def remove_dead_guilds_data(self):
        guild_ids = [guild.id for guild in self.bot.guilds]
        for guild_id in os.listdir("datas/guilds"):
            
            folder_path = os.path.join("datas/guilds", guild_id)
            if not int(guild_id) in guild_ids and time()-os.path.getmtime(folder_path) > 1296000: # 15days
                shutil.rmtree(folder_path)


def setup(bot):
    bot.add_cog(BackupCog(bot))