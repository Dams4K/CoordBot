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

        if command.name in self.commands:
            raise "Command already exist"

        self.commands[command.name] = command

    def get_command(self, name):
        return self.commands.get(name, None)

    def command(self, name = None, cls = None, *args, **kwargs):
        if cls is None:
            cls = Command

        def decorator(func: callable):
            command = cls(func, name=name, **kwargs)
            self.add_command(command)
            return command
        
        return decorator



class Command:
    def __init__(self, func: callable, **kwargs) -> None:
        self.callback = func
        self.cog = None
        
        name = kwargs.get("name") or func.__name__
        if not isinstance(name, str):
            raise TypeError("Name of a command must be a string.")
        self.name = name
    
    async def __call__(self, *args, **kwargs):
        if self.cog is not None:
            await self.callback(self.cog, *args, **kwargs) # cog is self
        else:
            await self.callback(*args, **kwargs)

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

class Terminal(Cog):
    def __init__(self) -> None:
        super().__init__()

        self.loop = asyncio.new_event_loop()
        self.can_listen = False
        self.thread = threading.Thread(target=self.run)

    def run(self):
        asyncio.ensure_future(self.listen_entries(), loop=self.loop)
        self.loop.run_forever()

    def start(self):
        self.thread.start()

    async def ainput(self, prompt: str = "") -> str:
        with ThreadPoolExecutor(1, "AsyncInput") as executor:
            return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).rstrip()

    async def listen_entries(self):
        while True:
            if not self.can_listen:
                continue

            entries = (await self.ainput("> ")).split(" ")
            cmd_name = entries[0]
            cmd_args = ()
            if len(entries) > 1:
                cmd_args = entries[1:]

            if cmd := self.commands.get(cmd_name):
                await cmd(*cmd_args)

def command(name = None, cls = None, *args, **kwargs):
    if cls == None:
        cls = Command
    
    def decorator(func: callable):
        command = cls(func, name=name, **kwargs)
        return command

    return decorator

if __name__ == "__main__":
    terminal = Terminal(None)

    @terminal.command()
    async def stop():
        print("stop")

    @terminal.command()
    async def say(*txt):
        print(" ".join(txt))

    terminal.start()