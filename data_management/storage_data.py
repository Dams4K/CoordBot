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


class Loot:
    def __init__(self, loot_id: int):
        self.loot_id = loot_id
        
    def add_item(self, item, weight):
        pass


class Item:
    @staticmethod
    def from_data(data):
        item = Item(data["name"])
        return item

    def __init__(self, name):
        self.name = name
    
    def __repr__(self): # same style as discord.py
        attrs = [
            ("item_name", self.name),
        ]
        inner = ' '.join("%s=%r" % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'

    def as_data(self):
        return {
            "name": self.name
        }


class Inventory:
    @staticmethod
    def from_data(data):
        inventory = Inventory(data["max_size"], [])
        for item_data in data["items"]:
            item = Item(item_data["name"])
            inventory.add_item(item)

        return inventory

    def __init__(self, max_size: int, items: list):
        self.max_size = max_size
        self.items = items

    def is_full(self):
        return len(self.items) >= self.max_size

    def add_item(self, item: Item):
        if self.is_full(): return

        self.items.append(item)
    
    def __repr__(self): # same style as discord.py
        attrs = [
            ("max_size", self.max_size),
            ("items", self.items)
        ]
        inner = ' '.join("%s=%r" % t for t in attrs)
        return f'<{self.__class__.__name__} {inner}>'

    def as_data(self):
        return {
            "max_size": self.max_size,
            "items": [item.as_data() for item in self.items]
        }


