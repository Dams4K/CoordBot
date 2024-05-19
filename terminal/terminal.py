class Cog:
    def __init__(self) -> None:
        self.commands = {}
        
        for method_name in dir(self):
            method = getattr(self, method_name)
            if isinstance(method, Command):
                method.cog = self
                self.add_command(method)

    def add_command(self, command):
        if not isinstance(command, Command):
            raise TypeError("The command passed must be a subclass of Command")

        command_name = command.name

        current_command = command
        while parent := current_command.parent:
            command_name = f"{parent.name} {command_name}"
            current_command = parent

        if command_name in self.commands:
            raise "Command already exist"

        self.commands[command_name] = command

    def get_command(self, name):
        return self.commands.get(name, None)

    def command(self, name = None, cls = None, *args, **kwargs):
        if cls is None:
            cls = Command

        def decorator(func: callable):
            command = cls(func, *args, name=name, **kwargs)
            self.add_command(command)
            return command
        
        return decorator

    def group(self, name = None, cls = None, *args, **kwargs):
        if cls is None:
            cls = Group

        def decorator(func: callable):
            command = cls(func, *args, name=name, **kwargs)
            return command
        
        return decorator


class Command:
    def __init__(self, func: callable, **kwargs) -> None:
        self.callback = func
        self.cog = None

        self.parent = kwargs.get("parent", None)
        
        name = kwargs.get("name") or func.__name__
        if not isinstance(name, str):
            raise TypeError("Name of a command must be a string.")
        self.name = name
    
    async def __call__(self, *args, **kwargs):
        if self.cog is not None:
            await self.callback(self.cog, *args, **kwargs) # cog is self
        else:
            await self.callback(*args, **kwargs)


class Group(Command):
    def __init__(self, func: callable, **kwargs) -> None:
        super().__init__(func, **kwargs)
        self.sub_commands = {}

    def get_command(self, cmd_name):
        return self.sub_commands.get(cmd_name)

    def command(self, name = None, cls = None, *args, **kwargs):
        if cls is None:
            cls = Command

        def decorator(func: callable):
            command = cls(func, name=name, parent=self, **kwargs)
            command.cog = self.cog
            self.sub_commands[command.name] = command
            return command
        
        return decorator


import asyncio
from concurrent.futures import ThreadPoolExecutor

class Terminal(Cog):
    def __init__(self) -> None:
        super().__init__()

        self.loop = asyncio.get_event_loop()
        self.can_listen = False

    def prepare(self):
        self.loop.create_task(self.listen_entries())

    def run(self):
        self.loop.run_forever()

    async def ainput(self, prompt: str = "") -> str:
        with ThreadPoolExecutor(1, "AsyncInput") as executor:
            return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).strip()

    async def listen_entries(self):
        while True:
            entry = await self.ainput("> ")
            if entry == "":
                continue
            
            entries = entry.split()

            cmd = self
            i = 0
            
            while (isinstance(cmd, Group) or isinstance(cmd, Cog)) and i < len(entries):
                cmd_name = entries[i]
                cmd = cmd.get_command(cmd_name)
                i += 1

            if not isinstance(cmd, Command):
                continue

            cmd_args = entries[i:]
            try:
                await cmd(*cmd_args)
            except Exception as e:
                print(e)

def command(name = None, cls = None, *args, **kwargs):
    if cls == None:
        cls = Command
    
    def decorator(func: callable):
        command = cls(func, name=name, **kwargs)
        return command

    return decorator

def group(name = None, cls = None, *args, **kwargs):
    if cls is None:
        cls = Group

    def decorator(func: callable):
        command = cls(func, *args, name=name, **kwargs)
        return command
    
    return decorator

if __name__ == "__main__":
    terminal = Terminal()
    terminal.can_listen = True

    @terminal.command()
    async def hello():
        print("world")

    @terminal.command()
    async def say(*txt):
        print(" ".join(txt))

    terminal.start()