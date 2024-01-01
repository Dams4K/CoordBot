import asyncio

from bot import CoordBot
from terminal import Terminal
from utils.references import References


class BotTerminal(Terminal):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

bot = CoordBot()
bot.load_cogs(References.COGS_FOLDER)

terminal = BotTerminal(bot)

@terminal.command()
async def test():
    print("ok")
    terminal.can_listen = False
    await asyncio.sleep(5)
    terminal.can_listen = True

@terminal.command()
async def hello():
    print("world")

terminal.can_listen = True
terminal.start()
bot.run(References.BOT_TOKEN)