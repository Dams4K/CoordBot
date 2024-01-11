import discord

from bot import CoordBot
from utils.bot_contexts import BotApplicationContext

class TestApplicationContext(BotApplicationContext):
    async def respond(self, *args, **kwargs):
        print(args, kwargs)

class TestBot(CoordBot):
    def __init__(self):
        super().__init__()
    
    async def on_ready(self):
        await super().on_ready()
        print("\n\tReady to test")

        await self.change_presence(status=discord.Status.dnd)

    async def on_application_command(self, ctx):
        print(type(ctx))

    async def get_application_context(self, interaction, cls = TestApplicationContext):
        return await super().get_application_context(interaction, cls=cls)