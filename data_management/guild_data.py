import discord
from ddm import *
from data_management import MemberData

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

    @Saveable.update()
    def pay_member(self, member: discord.Member) -> bool:
        """Pay a member

        Parameters
        ----------
            role: discord.Member

        Returns
        -------
            bool
                True: Member has been paid
                False: Member has not been paid
        """
        if not isinstance(member, discord.Member):
            return False

        best_pay = 0
        for role in member.roles:
            pay = self.salaries.get(str(role.id), 0)
            if pay > best_pay:
                best_pay = pay
        
        member_data = MemberData(member.id, self._guild_id)
        member_data.add_money(best_pay)
        return True
    
    @Saveable.update()
    def pay_role(self, role: discord.Role) -> bool:
        """Pay all members who have this role

        Parameters
        ----------
            role: discord.Role

        Returns
        -------
            bool
                True: all members have been paid
                False: No members have been paid
        """
        if not isinstance(role, discord.Role):
            return False

        for member in role.members:
            self.pay_member(member)
        return True

class GuildLevelingData(Saveable):
    def __init__(self, guild_id: int):
        self._guild_id = guild_id
        
        self.enabled = True
        self.level_up_message = "GG {member.mention} ! You just level up from `{level_before}` to `{level_after}`!!"
        self.formula = "LOLEELOLELEOLEOEL"
        self.channels_banned = []
        self.members_banned = []

        self.min_gain = 20
        self.max_gain = 30

        super().__init__(References.get_guild_folder(f"{self._guild_id}/leveling.json"))
    
    @Saveable.update()
    def enable(self):
        self.enabled = True
    @Saveable.update()
    def disable(self):
        self.enabled = False
    
    @Saveable.update()
    def set_level_up_message(self, new_message):
        self.level_up_message = new_message
    
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

    @Saveable.update()
    def set_min_gain(self, value):
        self.min_gain = value
    
    @Saveable.update()
    def set_max_gain(self, value):
        self.max_gain = value