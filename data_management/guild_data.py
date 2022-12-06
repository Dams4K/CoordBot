from .main import *
from utils.references import References

class GuildData(BaseData):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(get_guild_path(f"{self.guild_id}/global.json"))
    
    def load_base_data(self):
        self.data.setdefault("prefix", References.BOT_PREFIX)
        self.data.setdefault("xp_calculation", "{words}")
        self.data.setdefault("language", "en")

        # default member data
        self.default_member_data = {
            "member_xp": 0,
            "member_money": 0,
            "inventory_size": 10
        }
        self.data.setdefault("default_member_data", self.default_member_data)


    #- SETTERS
    @BaseData.manage_data
    def set_prefix(self, new_prefix: str):
        self.data["prefix"] = new_prefix
    
    @BaseData.manage_data
    def set_xp_calculation(self, new_calculation):
        self.data["xp_calculation"] = new_calculation

    @BaseData.manage_data
    def set_language(self, new_language):
        self.data["language"] = new_language


    @BaseData.manage_data
    def set_default_member_xp(self, value: int):
        self.default_member_data["member_xp"] = value
    @BaseData.manage_data
    def set_default_member_money(self, value: int):
        self.default_member_data["member_money"] = value
    
    @BaseData.manage_data
    def set_default_inventory_size(self, value: int):
        self.default_member_data["inventory_size"] = value




    #- PROPERTIES
    @property
    def prefix(self):
        self.load_base_data()
        return self.data["prefix"]
    
    @property
    def lang(self):
        self.load_base_data()
        return self.data["language"]
    
    @property
    def default_xp(self):
        self.load_base_data()
        return self.default_member_data["member_xp"]
    @property
    def default_money(self):
        self.load_base_data()
        return self.default_member_data["member_money"]
    
    @property
    def default_inventory_size(self):
        self.load_base_data()
        return self.default_member_data["inventory_size"]