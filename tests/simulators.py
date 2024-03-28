from discord.ext.commands import Cog

from .bot import TestBot

def test_options(**kwargs):
    def wrap(cmd):
        cmd.callback = get_test_callback(cmd.callback, **kwargs)
        return cmd

    return wrap

def get_test_callback(real_callback, **kwargs):
    async def inner_callback(self, ctx, *a, **k): # we don't care about `a` and `k`
        await real_callback(self=self, ctx=ctx, **kwargs)
    
    if TestBot.RUNNING:
        return inner_callback
    return real_callback