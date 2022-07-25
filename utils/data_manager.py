import os
import json
import random
from utils.references import References

BASE_GUILD_FOLDER = "datas/guilds/"

def get_guild_path(*end):
    return os.path.join(BASE_GUILD_FOLDER, *end)

class BaseData:
    def __init__(self, file_path, base_data = {}):
        self.file_path = file_path

        self.data = base_data if not hasattr(self, "data") else self.data
        self.load()


    def create_dirs(self):
        dirname = os.path.dirname(self.file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)


    def load_base_data(self): pass


    def load(self):
        self.create_dirs()
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
        else:
            self.save()


    def save(self):
        data = self.get_data()
        self.create_dirs()
        if data != None:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
    

    def get_data(self):
        return self.data.copy()

    def manage_data(func):
        def decorator(self, *args, **kwargs):
            self.load()
            self.load_base_data()

            result = func(self, *args, **kwargs)
            
            self.save()
            
            return result
        return decorator


class GuildData(BaseData):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        super().__init__(get_guild_path(f"{self.guild_id}/global.json"))
    
    def load_base_data(self):
        self.data.setdefault("prefix", References.BOT_PREFIX)
        self.data.setdefault("xp_calculation", "{words}")

    @BaseData.manage_data
    def set_prefix(self, new_prefix: str):
        self.data["prefix"] = new_prefix
    

    @BaseData.manage_data
    def set_xp_calculation(self, new_calculation):
        self.data["xp_calculation"] = new_calculation


    def get_prefix(self):
        return self.data["prefix"]


class MemberData(BaseData):
    def __init__(self, guild_id, member_id):
        self.guild_id = guild_id
        self.member_id = member_id
        super().__init__(get_guild_path(f"{self.guild_id}/members/{self.member_id}.json"))
    
    def load_base_data(self):
        self.data.setdefault("xp", 0)
        self.data.setdefault("money", 0)

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
    pass