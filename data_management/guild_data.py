import csv
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

    @Saveable.update()
    def add_translation(self, key, value) -> None:
        self.rows.setdefault(key, value)

    @Saveable.update()
    def remove_translation(self, key) -> str:
        pass


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