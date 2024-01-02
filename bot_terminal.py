from terminal import Terminal, command

class BotTerminal(Terminal):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.can_listen = True
    
    @command()
    async def hello(self):
        print("world")
    
    @command(name="botname")
    async def bot_name(self):
        print(self.bot.user.name)