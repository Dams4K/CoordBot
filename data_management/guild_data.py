import discord

from data_management import MemberData
from ddm import *
from utils.references import References


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class GuildConfig(Saveable):
    __slots__ = ("_guild_id", "prefix", "language")

    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.prefix = References.BOT_PREFIX
        self.language = "en"

        super().__init__(References.get_guild_folder(f"{self._guild_id}/global.json"))
    

    #- SETTERS
    @Saveable.update()
    def set_prefix(self, value: str):
        self.prefix = value
    
    @Saveable.update()
    def set_language(self, value):
        self.language = value


class GuildLanguage(Saveable):
    __slots__ = ("_guild_id", "rows")

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
    __slots__ = ("_guild_id", "salaries")
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
    async def fetch_salaries(self, guild: discord.Guild) -> list:
        roles = []
        pays = []

        dead_role_ids = []

        dead_roles = []
        guild_roles = {str(role.id): role for role in await guild.fetch_roles()}

        for role_id, pay in self.salaries.items():
            if role_id in guild_roles:
                roles.append(guild_roles[role_id])
                pays.append(pay)
            else:
                dead_role_ids.append(role_id)
        
        for role_id in dead_role_ids:
            self.salaries.pop(role_id)
        
        return (roles, pays)

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

        best_pay = None
        for role in member.roles:
            pay = self.salaries.get(str(role.id), None)
            if not best_pay or (pay and pay > best_pay):
                best_pay = pay
        
        member_data = MemberData(member.id, self._guild_id)
        
        if best_pay:
            member_data.add_money(best_pay)
            return True
        return False
    
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

class GuildLevelingConfig(Saveable):
    __slots__ = ("_guild_id", "enabled", "message", "formula", "banned_channels", "banned_members", "min_gain", "max_gain")

    def __init__(self, guild_id: int):
        self._guild_id = guild_id
        
        self.enabled = True
        self.message = "GG {member.mention} ! You've just reached level `{level_after}` and earned {earned_money} coins!!"
        self.formula = "20*(level+1)"
        self.banned_channels = []
        self.banned_members = []

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
    def set_message(self, value: str):
        self.message = value[:512]
    
    def get_message(self, **kwargs):
        return self.message.format_map(FormatDict(kwargs))

    @Saveable.update()
    def set_formula(self, value):
        self.formula = value

    @Saveable.update()
    def ban_channel(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return
        if channel.id in self.banned_channels:
            return
        
        self.banned_channels.append(channel.id)
        
    @Saveable.update()
    def unban_channel(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return
        if not channel.id in self.banned_channels:
            return
        
        self.banned_channels.remove(channel.id)
    
    def is_channel_ban(self, channel: discord.TextChannel):
        if not isinstance(channel, discord.TextChannel):
            return False
        
        return channel.id in self.banned_channels
    
    @Saveable.update()
    def ban_member(self, member: discord.Member): # return error
        if not isinstance(member, discord.Member):
            return
        if member.id in self.banned_members:
            return
        
        self.banned_members.append(member.id)

    @Saveable.update()
    def unban_member(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            return
        if not member.id in self.banned_members:
            return
        
        self.banned_members.remove(member.id)

    def is_member_ban(self, member: discord.Member):
        if not isinstance(member, discord.Member):
            return False
        
        return member.id in self.banned_members

    @Saveable.update()
    def set_min_gain(self, value):
        self.min_gain = value
    
    @Saveable.update()
    def set_max_gain(self, value):
        self.max_gain = value
