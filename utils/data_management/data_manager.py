import random
from .main import *


class ChestData(BaseData):
    def __init__(self, guild_id, chest_id = -1):
        self.guild_id = guild_id

        if chest_id == -1:
            dirname = get_guild_path(f"{self.guild_id}/chests")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            chests_id = [-1] + [int(i.split(".")[0]) for i in os.listdir(dirname)]
            chest_id = sorted(chests_id)[-1]+1

        self.chest_id = chest_id
        super().__init__(get_guild_path(f"{self.guild_id}/chests/{self.chest_id}.json"))

    def load_base_data(self):
        self.data.setdefault("name", "no name")

    @BaseData.manage_data
    def set_name(self, new_name):
        self.data["name"] = new_name

    @BaseData.manage_data
    def add_loot(self, loot):
        pass
    
    @BaseData.manage_data
    def remove_loot(self, loot):
        pass


    @property
    def name(self):
        self.load_base_data()
        return self.data["name"]

    @property
    def loots(self):
        pass


    def open(self):
        pass

    def delete(self):
        os.remove(self.file_path)


class Inventory:
    pass


class Loot:
    def __init__(self, loot_id: int):
        self.loot_id = loot_id
        
    def add_item(self, item, weight):
        pass


class Item:
    pass