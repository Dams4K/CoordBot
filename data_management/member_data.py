import copy

from simpleeval import simple_eval

from ddm import *
from utils.references import References

from .storage_data import Inventory


class DefaultMemberData(Saveable):
    __slots__ = ("_guild_id", "xp", "level", "money", "inventory")

    def __init__(self, guild_id):
        self._guild_id = guild_id

        self.xp = 0
        self.level = 0
        self.money = 0
        self.inventory = Inventory()

        super().__init__(References.get_guild_folder(f"{self._guild_id}/members/default.json"))

    @Saveable.update()
    def set_xp(self, amount: int):
        self.xp = amount
    
    @Saveable.update()
    def set_level(self, amount: int):
        self.level = amount

    @Saveable.update()
    def set_money(self, amount: int):
        self.money = amount

    def get_inventory(self) -> Inventory:
        return copy.copy(self.inventory)
    
    @Saveable.update()
    def set_inventory(self, new_inventory: Inventory):
        self.inventory = new_inventory


class MemberData(DefaultMemberData):
    __slots__ = ("_member_id",)

    def __init__(self, member_id, guild_id):
        self._member_id = member_id
        self._guild_id = guild_id

        DefaultMemberData.__init__(self, guild_id)
        Saveable.__init__(self, References.get_guild_folder(f"{self._guild_id}/members/{self._member_id}.json"))
    
    def get_xp_goal(self, formula):
        return simple_eval(formula, names={"level": self.level})

    def refresh_level(self, formula) -> int:
        xp_needed = self.get_xp_goal(formula)
        if self.xp >= xp_needed:
            self.add_level(1)
            self.add_xp(-xp_needed)
            return self.refresh_level(formula)
        return self.level

    @Saveable.update()
    def add_xp(self, amount: int):
        self.xp += amount

    @Saveable.update()
    def add_level(self, amount: int):
        self.level += amount
    
    @Saveable.update()
    def add_money(self, amount: int):
        self.money += amount