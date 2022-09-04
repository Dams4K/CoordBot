import asyncio
from concurrent.futures import ThreadPoolExecutor

class Terminal:
    def __init__(self, prefix = " > "):
        self.prefix = prefix
        self.commands = {}
        self.loop = asyncio.get_event_loop()

    async def start(self):
        await self.loop.run_until_complete(await self.entry_loop())
    async def entry_loop(self):
        while True:
            cmd_name = await self.ainput(self.prefix)
            command = self.commands.get(cmd_name)
            if command is None:
                for cmd in self.commands.values():
                    if cmd_name in cmd.aliases:
                        command = cmd
            if command is None: continue

            await command.call_func()
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
            result = Command(name, func, **kwargs)
            self.add_command(result)
            return result
        return decorator


class Command:
    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.aliases = kwargs.get("aliases", [])
        self.cog = None
    
    async def call_func(self):
        assert self.cog is not None, "cog ins't set"
        await self.func(self.cog)
    

    def set_cog(self, cog):
        self.cog = cog