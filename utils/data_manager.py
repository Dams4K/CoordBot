import os
import json

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

            result = func(self, *args, **kwargs)
            
            self.save()
            
            return result
        return decorator


class GuildData(BaseData):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.data = {}
        super().__init__(get_guild_path(f"{self.guild_id}/global.json"))

class MemberData(BaseData):
    def __init__(self, guild_id, member_id):
        self.guild_id = guild_id
        self.member_id = member_id
        self.data = {}
        super().__init__(get_guild_path(f"{self.guild_id}/members/{self.member_id}.json"))