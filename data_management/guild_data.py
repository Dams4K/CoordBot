import discord
from ddm import *
from utils.references import References

class GuildConfig(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.prefix = References.BOT_PREFIX
        self.xp_calculation = "{words}"
        self.language = "en"
        self.level_system_enabled = True
        self.leveling_formula = "20*({l}+1)" #maybe later, level**2+C
        self.level_up_message = "GG {member.mention} ! You just level up from `{level_before}` to `{level_after}`!!"

        super().__init__(References.get_guild_folder(f"{self._guild_id}/global.json"))
    

    #- SETTERS
    @Saveable.update()
    def set_prefix(self, new_prefix: str):
        self.prefix = new_prefix
    
    @Saveable.update()
    def set_xp_calculation(self, new_calculation):
        self.xp_calculation = new_calculation

    @Saveable.update()
    def set_language(self, new_language):
        self.language = new_language

    @Saveable.update()
    def enable_level_system(self, value):
        self.level_system_enabled = value
    @Saveable.update()
    def set_leveling_formula(self, formula):
        self.leveling_formula = formula
    

    def send_level_up_message(self, m, lb, la):
        return self.level_up_message.format(member=m, level_before=lb, level_after=la)


class GuildLanguage(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id

        self.rows = {}

        super().__init__(References.get_guild_folder(f"{self._guild_id}/lang.json"))

    def get_keys(self) -> list[str]:
        return list(self.rows.keys())

    @Saveable.update()
    def add_translation(self, key, translation) -> None:
        self.rows[key.upper()] = translation

    @Saveable.update()
    def reset_translation(self, key) -> str:
        if key.upper() in self.rows:
            return self.rows.pop(key.upper())


class GuildDefaultMemberData(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.xp = 0
        self.level = 0
        self.money = 0
        self.inventory_size = 10

        super().__init__(References.get_guild_folder(f"{self._guild_id}/default_member.json"))

    @Saveable.update()
    def set_xp(self, value: int):
        self.xp = value
    @Saveable.update()
    def set_level(self, value: int):
        self.level = level
    @Saveable.update()
    def set_money(self, value: int):
        self.money = value
    
    @Saveable.update()
    def set_inventory_size(self, value: int):
        self.inventory_size = value

class GuildSalaries(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.salaries = {}

        super().__init__(References.get_guild_folder(f"{self._guild_id}/salaries.json"))
    
    @Saveable.update()
    def add_salary(self, role: discord.Role, pay: int):
        self.salaries[str(role.id)] = pay
    
    @Saveable.update()
    def remove_salary(self, role: discord.Role):
        role_id = str(role.id)
        if role_id in self.salaries:
            self.salaries.pop(role_id)

class GuildLevelingData(Saveable):
    def __init__(self, guild_id: int):
        self._guild_id = guild_id
        
        self.enabled = True
        self.levelup_message = "GG {member.mention} ! You just level up from `{level_before}` to `{level_after}`!!"
        self.channels_banned = []
        self.members_banned = []

        super().__init__(References.get_guild_folder(f"{self._guild_id}/leveling.json"))
    
    @Saveable.update()
    def enable(self):
        self.enabled = True
    @Saveable.update()
    def disable(self):
        self.enabled = False
    
    @Saveable.update()
    def set_levelup_message(self, new_message):
        self.levelup_message = new_message
    
    @Saveable.update()
    def ban_channel(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return
        if channel.id in self.channels_banned:
            return
        
        self.channels_banned.append(channel.id)
        
    @Saveable.update()
    def unban_channel(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return
        if not channel.id in self.channels_banned:
            return
        
        self.channels_banned.remove(channel.id)
    
    def is_channel_ban(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return False
        
        return channel.id in self.channels_banned
    
    @Saveable.update()
    def ban_member(self, member: discord.Member): # return error
        if not isinstance(member, discord.Member):
            return
        if member.id in self.members_banned:
            return
        
        self.members_banned.append(member.id)

    @Saveable.update()
    def unban_member(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            return
        if not member.id in self.members_banned:
            return
        
        self.members_banned.remove(member.id)

    def is_member_ban(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            return False
        
        return member.id in self.members_banned