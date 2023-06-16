from bot import CoordBot
from utils.references import References

bot = CoordBot()
bot.load_cogs(References.COGS_FOLDER)
bot.run(References.BOT_TOKEN)