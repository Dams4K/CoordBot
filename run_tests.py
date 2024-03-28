from tests import TestBot
from utils.references import References

bot = TestBot()
bot.load_cogs(References.COGS_FOLDER)
bot.run(References.BOT_TOKEN)