from .main import *
from .guild_data import GuildData
from .storage_data import Inventory

class MemberData(BaseData):
    def __init__(self, guild_id, member_id):
        self.guild_id = guild_id
        self.member_id = member_id

        super().__init__(get_guild_path(f"{self.guild_id}/members/{self.member_id}.json")) # load stored data
        self.load_base_data() # load default data (after init because self.data did not exist before)
    
    def load_base_data(self):
        guild_data = GuildData(self.guild_id)
        self.data.setdefault("xp", guild_data.default_xp)
        self.data.setdefault("money", guild_data.default_money)
        self.data.setdefault("inventory", Inventory(guild_data.default_inventory_size, []).as_data())

    @BaseData.manage_data
    def add_xp(self, amount: int):
        self.data["xp"] += amount
    @BaseData.manage_data
    def set_xp(self, amount: int):
        self.data["xp"] = amount
    

    @BaseData.manage_data
    def add_money(self, amount: int):
        self.data["money"] += amount
    @BaseData.manage_data
    def set_money(self, amount: int):
        self.data["money"] = amount

    def get_inventory(self) -> Inventory:
        return Inventory.from_data(self.data["inventory"])
    @BaseData.manage_data
    def set_inventory(self, inventory: Inventory):
        self.data["inventory"] = inventory.as_data()


    def reset(self):
        os.remove(self.file_path)


    @property
    def xp(self):
        self.load_base_data()
        return self.data["xp"]
    @property
    def money(self):
        self.load_base_data()
        return self.data["money"]
