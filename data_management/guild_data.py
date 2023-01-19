from .main import *
from .storage_data import Item
from utils.references import References

from ddm import *

class GuildConfig(Saveable):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(get_guild_path(f"{self.guild_id}/global.json"))
        
        self.prefix = References.BOT_PREFIX
        self.xp_calculation = "{words}"
        self.language = "en"
    

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


    @property
    def lang(self):
        return self.data["language"]


class GuildDefaultMemberData(BaseData):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(get_guild_path(f"{self.guild_id}/default_member.json"), {})
        self.load_base_data()

    def load_base_data(self):
        self.data.setdefault("xp", 0)
        self.data.setdefault("money", 0)
        self.data.setdefault("inventory_size", 10)
    
    @BaseData.manage_data
    def set_default_xp(self, value: int):
        self.data["xp"] = value
    @BaseData.manage_data
    def set_default_money(self, value: int):
        self.data["money"] = value
    
    @BaseData.manage_data
    def set_default_inventory_size(self, value: int):
        self.data["inventory_size"] = value
    
    @property
    def default_xp(self):
        self.load_base_data()
        return self.data["xp"]
    @property
    def default_money(self):
        self.load_base_data()
        return self.data["money"]
    
    @property
    def default_inventory_size(self):
        self.load_base_data()
        return self.data["inventory_size"]


class GuildStorageConfig(BaseData):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(get_guild_path(f"{self.guild_id}/storage_config.json"), {})
        self.load_base_data()

    def load_base_data(self):
        self.data.setdefault("items", [])
    
    def get_items(self):
        items = []
        for item_data in self.data["items"]:
            items.append(Item.from_data(item_data))
        return items
    
    def find_item(self, item_id: str):
        for item_data in self.data["items"]:
            if item_data["id"] == item_id:
                return Item.from_data(item_data)

    @BaseData.manage_data
    def create_item(self, item: Item):
        self.data["items"].append(item.as_data())
    @BaseData.manage_data
    def delete_item(self, item: Item):
        self.data["items"].remove(item.as_data())