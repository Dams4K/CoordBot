from .main import *
from .storage_data import Item
from utils.references import References

from ddm import *

class GuildConfig(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.prefix = References.BOT_PREFIX
        self.xp_calculation = "{words}"
        self.language = "en"

        super().__init__(get_guild_path(f"{self._guild_id}/global.json"))
    

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



class GuildDefaultMemberData(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.xp = 0
        self.money = 0
        self.inventory_size = 10

        super().__init__(get_guild_path(f"{self._guild_id}/default_member.json"))

    @Saveable.update()
    def set_xp(self, value: int):
        self.xp = value
    @Saveable.update()
    def set_money(self, value: int):
        self.money = value
    
    @Saveable.update()
    def set_inventory_size(self, value: int):
        self.inventory_size = value


class GuildStorageConfig(Saveable):
    def __init__(self, guild_id):
        self._guild_id = guild_id
        self.items = []
        self._items_type = Item()

        super().__init__(get_guild_path(f"{self._guild_id}/storage_config.json"))

    
    def find_item(self, item_id: str):
        for item in self.items:
            if item.id == item_id:
                return item

    @Saveable.update()
    def create_item(self, item: Item):
        self.items.append(item)
    
    @Saveable.update()
    def delete_item(self, item: Item):
        self.items.remove(item)