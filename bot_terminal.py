import discord
import os, sys

from cogs.tasks.analyzer import AnalyzerCog

from terminal import Terminal, command, group

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class BotTerminal(Terminal):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot
        self.can_listen = True

    @command()
    async def help(self):
        print(
f"""{Color.BOLD}=== HELP PAGE ==={Color.END}

extensions
extension
    unload  {{path}}
    load    {{path}}
    reload  {{path}}
stop
memory
""")
     
    @command()
    async def extensions(self):
        available_extensions: list = self.bot.available_extensions
        enabled_extensions: list = self.bot.extensions.keys()

        l = []
        for ex in available_extensions:
            status = Color.GREEN + Color.BOLD + "ENABLED" + Color.END
            if ex not in enabled_extensions:
                status = Color.RED + Color.BOLD + "DISABLED" + Color.END

            l.append(f"{ex} {status}")
        print("\n".join(l))
    
    @group()
    async def extension(self):
        subcommands = "\t".join(self.extension.sub_commands.keys())
        print(f"Subcommands: {subcommands}")
    
    @extension.command()
    async def unload(self, extension):
        if extension in self.bot.available_extensions:
            self.bot.unload_extension(extension)
            print("extension unloaded")
        else:
            print("unknown extension")

    @extension.command()
    async def load(self, extension):
        if extension in self.bot.available_extensions:
            self.bot.load_extension(extension)
            print("extension loaded")
        else:
            print("unknown extension")
    
    @extension.command()
    async def reload(self, extension):
        if extension in self.bot.available_extensions:
            self.bot.reload_extension(extension)
            print("extension reloaded")
        else:
            print("unknown extension")

    @command()
    async def stop(self):
        await self.bot.close()
    
    @command()
    async def memory(self):
        print(f"""Memory Usage
Current: {self.bot.MEM_USAGE}
Max: {self.bot.MAX_MEM_USAGE}
""")