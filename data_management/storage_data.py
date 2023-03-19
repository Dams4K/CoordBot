import random
from ddm import *
from utils.references import References

class ChestData(Saveable):
    def __init__(self, guild_id, chest_name: str = "No name", chest_id = -1):
        self._guild_id = guild_id

        # create the next id usable
        if chest_id == -1:
            dirname = References.get_guild_folder(f"{self._guild_id}/chests")
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            chests_id = [-1] + [int(i.split(".")[0]) for i in os.listdir(dirname)]
            chest_id = sorted(chests_id)[-1]+1

        self._chest_id = chest_id
        self.name = chest_name

        super().__init__(References.get_guild_folder(f"{self._guild_id}/chests/{self._chest_id}.json"))

    @Saveable.update()
    def set_name(self, new_name):
        self.name = new_name

    @Saveable.update()
    def add_loot(self, loot):
        pass
    
    @Saveable.update()
    def remove_loot(self, loot):
        pass

    def open(self):
        pass

    def delete(self):
        os.remove(self.file_path)


class Loot(Saveable):
    def __init__(self, loot_id: int, guild_id: int):
        self._loot_id = loot_id
        self._guild_id = guild_id

        super().__init__(References.get_guild_folder(f"{guild_id}/loots/{loot_id}.json"))
        
    def add_item(self, item, weight):
        pass


class Item(Data):
    def __init__(self, item_id: str = "no_id", item_name: str = "no_name"):
        self.id = item_id
        self.name = item_name

        super().__init__()


class Inventory(Data):
    def __init__(self, max_size: int, items: list):
        self.max_size = max_size
        self.items = items
        self._items_type = Item()

    def is_full(self):
        return len(self.items) >= self.max_size

    def add_item(self, item: Item, amount: int):
        if self.is_full(): return
        
        self.items.extend([item] * amount)
    
    def remove_item(self, item_id, amount: int):
        if amount == -1:
            amount = len(self.items)
        n = 0
        while n < amount:
            if not item_id in self.items: break
            self.items.remove(item_id)
            n += 1

    def get_items(self):
        return self.items


class GuildArticle(Saveable):
    FOLDER: str = "%s/articles"
    FILENAME: str = "%s.json"

    @staticmethod
    def new(guild_id: int, article_name: str):
        new_id = 0
        articles_folder = References.get_guild_folder(GuildArticle.FOLDER % guild_id)
        if os.path.exists(articles_folder):
            ids = [int(filename.replace(".json", "")) for filename in os.listdir(articles_folder)]
            new_id = max(ids)+1
        return GuildArticle(new_id, guild_id)

    def __init__(self, article_id, guild_id):
        self._article_id = article_id
        self._guild_id = guild_id
        self.price: float = 0
        
        super().__init__(References.get_guild_folder(os.path.join(GuildArticle.FOLDER % self._guild_id, GuildArticle.FILENAME % self._article_id)))

    @Saveable.update()
    def set_price(self, new_price: float):
        self.price = new_price