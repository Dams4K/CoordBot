from bot import CoordBot
from bot_terminal import BotTerminal
from utils.references import References

bot = CoordBot()
bot.load_cogs(References.COGS_FOLDER)

terminal = BotTerminal(bot)
terminal.loop = bot.loop
terminal.prepare()

bot.run(References.BOT_TOKEN)