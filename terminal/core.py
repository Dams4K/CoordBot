import asyncio
from concurrent.futures import ThreadPoolExecutor


class Command:
    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.aliases = kwargs.get("aliases", [])
        self.cog = None
    
    async def invoke(self):
        # assert self.cog is not None, "cog ins't set"
        if self.cog:
            await self.func(self.cog)
        else:            
            await self.func()
    

    def set_cog(self, cog):
        self.cog = cog

class Cog:
    def __init__(self) -> None:
        pass

class Terminal:
    def __init__(self, prefix = " > "):
        self.prefix = prefix
        self.commands = {}
        self.loop = asyncio.get_event_loop()

    async def start(self):
        await self.loop.run_until_complete(await self.entry_loop())
    
    async def entry_loop(self):
        while True:
            cmd_discriminator = await self.ainput(self.prefix)
            
            if command := self.get_command(cmd_discriminator):
                await command.invoke()
    
    async def ainput(self, prompt: str = "") -> str:
        with ThreadPoolExecutor(1, "AsyncInput") as executor:
            return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

    def inject_cog(self, cog):
        for command in self.commands.values():
            command.set_cog(cog)

    def add_command(self, command):
        self.commands[command.name] = command

    def command(self, name, **kwargs):
        def decorator(func):
            command = Command(name, func, **kwargs)
            self.add_command(command)
            return command
        return decorator

    def get_command(self, discriminator: str) -> Command:
        # Priority to names
        if cmd := self.commands.get(discriminator):
            return cmd

        # If discriminator isn't a name, we check all the aliases
        for cmd in self.commands.values():
            if discriminator in cmd.aliases:
                return cmd
        return None