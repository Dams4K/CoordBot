from tests import TestBot
from utils.references import References

bot = TestBot()
bot.load_cogs(References.COGS_FOLDER)


# @bot.command(name="tests")
# async def tests(ctx):
#     for cmd in bot.all_commands.values():
#         print(cmd)

bot.run(References.BOT_TOKEN)