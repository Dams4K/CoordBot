import copy

from .main import *
from .guild_data import GuildDefaultMemberData
from .storage_data import Inventory

from ddm import *

class MemberData(Saveable):
    def __init__(self, guild_id, member_id):
        self._guild_id = guild_id
        self._member_id = member_id

        guild_default_member = GuildDefaultMemberData(self._guild_id)
        self.xp = guild_default_member.xp
        self.money = guild_default_member.xp
        self.inventory = Inventory(guild_default_member.inventory_size, [])

        super().__init__(get_guild_path(f"{self._guild_id}/members/{self._member_id}.json"))
    
    @Saveable.update()
    def add_xp(self, amount: int):
        self.xp += amount
    
    @Saveable.update()
    def set_xp(self, amount: int):
        self.xp = amount
    

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
        os.remove(self.file_path)