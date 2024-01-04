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
        self.bot = bot
        self.can_listen = True

        print(self.extension)

    @command()
    async def hello(self):
        print("world")
     
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
        print("group")
    
    @extension.command()
    async def load(self, n):
        print("load", n)