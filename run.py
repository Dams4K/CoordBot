from bot import ElricBot
from utils.references import References

bot = ElricBot()
bot.load_cogs(References.COGS_FOLDER)
bot.run(References.BOT_TOKEN)