from ddm import *
from .guild_data import GuildDefaultMemberData
from .storage_data import Inventory
from utils.references import References
import copy

class MemberData(Saveable):
    def __init__(self, guild_id, member_id):
        self._guild_id = guild_id
        self._member_id = member_id

        guild_default_member = GuildDefaultMemberData(self._guild_id)
        self.xp = guild_default_member.xp
        self.level = guild_default_member.level
        self.money = guild_default_member.xp
        self.inventory = Inventory(guild_default_member.inventory_size, [])

        super().__init__(References.get_guild_folder(f"{self._guild_id}/members/{self._member_id}.json"))
    
    @Saveable.update()
    def add_xp(self, amount: int):
        self.xp += amount
    
    @Saveable.update()
    def set_xp(self, amount: int):
        self.xp = amount
    
    def get_xp_goal(self, leveling_formula):
        return eval(leveling_formula.format(l=self.level)) #TODO: check if `leveling_formula` have only number and {level} inside, else python injection can be done

    def refresh_level(self, leveling_formula) -> int:
        xp_needed = self.get_xp_goal(leveling_formula)
        if self.xp >= xp_needed:
            self.add_level(1)
            self.add_xp(-xp_needed)
            return self.refresh_level(leveling_formula)
        return self.level

    @Saveable.update()
    def add_level(self, amount: int):
        self.level += amount
    
    @Saveable.update()
    def set_level(self, amount: int):
        self.level = amount

    @Saveable.update()
    def add_money(self, amount: int):
        self.money += amount

    @Saveable.update()
    def set_money(self, amount: int):
        self.money = amount

    def get_inventory(self) -> Inventory:
        return copy.copy(self.inventory)
    
    @Saveable.update()
    def set_inventory(self, new_inventory: Inventory):
        self.inventory = new_inventory


    def reset(self):
        os.remove(self._path)