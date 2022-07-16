class BaseData:
    def __init__(self, file_path, base_data = {}):
        self.file_path = file_path
        self.data = base_data if not hasattr(self, "data") else self.data
        self.load_data()


    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
        else:
            self.save_data()


    def save(self):
        data = self.get_data()
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


class MemberData(BaseData):
    def __init__(self, member_id):
        self.xp = 0

    def add_xp(self, amount):
        self.xp += amount
    def set_xp(self, amount):
        self.xp = amount
    
    """
    calcul level of the member based of his xp amount
    """
    def get_level(self):
        pass