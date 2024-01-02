from bot import CoordBot
from bot_terminal import BotTerminal
from utils.references import References




bot = CoordBot()
bot.load_cogs(References.COGS_FOLDER)

terminal = BotTerminal(bot)
terminal.start()
bot.run(References.BOT_TOKEN)