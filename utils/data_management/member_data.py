from .main import *

class MemberData(BaseData):
    def __init__(self, guild_id, member_id):
        self.guild_id = guild_id
        self.member_id = member_id

        super().__init__(get_guild_path(f"{self.guild_id}/members/{self.member_id}.json")) # load stored data
        self.load_base_data() # load default data (after init because self.data did not exist before)
    
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
