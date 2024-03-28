import discord
from discord.ext import commands

from bot import CoordBot
from utils.bot_contexts import BotApplicationContext

class TestInteraction(discord.Interaction):
    pass

class TestGuild(discord.Guild):
    pass

class TestApplicationContext(BotApplicationContext):
    def __init__(self):
        super().__init__()

    async def respond(self, *args, **kwargs):
        # print(args, kwargs)
        pass

    async def send(self, *args, **kwargs):
        pass

class TestBot(CoordBot):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        self.add_cog(TestCog(self))

        await super().on_ready()
        print("\n\tReady to test")

        await self.change_presence(status=discord.Status.dnd)

    async def on_application_command(self, ctx):
        print(type(ctx))

    async def get_application_context(self, interaction, cls = TestApplicationContext):
        return await super().get_application_context(interaction, cls=cls)

class TestCog(discord.Cog):
    def __init__(self, bot) -> None:
        self.bot: discord.Bot = bot

    @commands.command(name="tests")
    async def tests(self, ctx):
        print(len(self.bot.application_commands))
        print(len(self.bot.commands))
        print(len(self.bot.all_commands))