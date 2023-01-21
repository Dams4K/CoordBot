import discord
from discord.ext.bridge import BridgeContext, BridgeExtContext, BridgeApplicationContext
from data_management import GuildConfig, MemberData
from lang import Lang

class BotBridgeContext(BridgeContext):
    @property
    def guild_config(self):
        return GuildConfig(self.guild.id)
    @property
    def author_data(self):
        return MemberData(self.guild.id, self.user.id)
    
    async def translate(self, text_key: str, *args, **kwargs):
        return Lang.get_text(text_key, self.guild_config.language, *args, **kwargs)
    
    async def translate_message(self, *args, **kwargs):
        text_key = kwargs.pop("text_key", None)
        text_args = kwargs.pop("text_args", {})
        if not text_key is None:
            translated_text = Lang.get_text(text_key, self.guild_config.language, **text_args)
            if "content" in kwargs:
                kwargs["content"] += translated_text
            else:
                args = list(args)
                if len(args) > 0:
                    args[0] += translated_text
                else:
                    args.append(translated_text)
                args = tuple(args)
        
        return args, kwargs

class BotApplicationContext(BridgeApplicationContext, BotBridgeContext):
    async def respond(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        await super().respond(*args, **kwargs)
    
    async def send(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        await super().send(*args, **kwargs)

class BotContext(BridgeExtContext, BotBridgeContext):
    async def send(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        await super().send(*args, **kwargs)