import discord
from discord.ext import commands

from bot import CoordBot
from utils.bot_contexts import BotApplicationContext, BotContext

class TestInteraction(discord.Interaction):
    pass

class TestGuild(discord.Guild):
    pass

class TestApplicationContext(BotApplicationContext):
    def __init__(self):
        super().__init__()

    async def respond(self, *args, **kwargs):
        print('----')
        print(args, kwargs)

    async def send(self, *args, **kwargs):
        print(args, kwargs)

class TestContext(BotContext):
    async def send(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        print(*args, **kwargs)
    
    async def respond(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        print(*args, **kwargs)

class TestBot(CoordBot):
    RUNNING = False

    def __init__(self):
        TestBot.RUNNING = True
        super().__init__()

    async def on_ready(self):
        self.add_cog(TestCog(self))

        await super().on_ready()
        print("\n\tReady to test")

        await self.change_presence(status=discord.Status.dnd)

    async def get_application_context(self, interaction, cls=TestApplicationContext):
        return await super().get_application_context(interaction, cls=cls)

    async def get_context(self, message, *, cls=TestContext):
        return await super().get_context(message, cls=cls)

class TestCog(discord.Cog):
    def __init__(self, bot) -> None:
        self.bot: discord.Bot = bot

    @commands.command(name="tests")
    async def tests(self, ctx):
        for cmd in self.bot.all_commands:
            await cmd(ctx)