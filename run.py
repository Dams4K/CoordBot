from bot import GDCPBot
from utils.references import References

bot = GDCPBot()
bot.load_cogs(References.COGS_FOLDER)
bot.run(References.BOT_TOKEN)