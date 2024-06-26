from discord.commands.context import AutocompleteContext
from discord.ext.bridge import (BridgeApplicationContext, BridgeContext,
                                BridgeExtContext)

from data_management import GuildConfig, GuildLanguage, MemberData
from lang import Lang


class BotBridgeContext(BridgeContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.guild_config = None
        self.author_data = None
        if self.guild:
            self.guild_config = GuildConfig(self.guild.id)
            self.author_data = MemberData(self.user.id if hasattr(self, "user") else self.author.id, self.guild.id)

    def translate(self, text_key: str, *args, **kwargs):
        if self.guild_config is None:
            return Lang.get_text(text_key, "en", *args, **kwargs)
        else:
            custom_translations = GuildLanguage(self.guild.id) # Maybe do something different because it loads the file way too frequently
            return Lang.get_text(text_key, self.guild_config.language, custom_rows=custom_translations.rows, *args, **kwargs)
    
    async def translate_message(self, *args, **kwargs):
        text_key = kwargs.pop("text_key", None)
        text_args = kwargs.pop("text_args", {})
        if not text_key is None:
            translated_text = self.translate(text_key, **text_args)
            
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

    async def send(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        return await super().send(*args, **kwargs)
    
    async def respond(self, *args, **kwargs):
        args, kwargs = await self.translate_message(*args, **kwargs)
        return await super().respond(*args, **kwargs)

class BotApplicationContext(BridgeApplicationContext, BotBridgeContext):
    pass

class BotContext(BridgeExtContext, BotBridgeContext):
    pass

class BotAutocompleteContext(AutocompleteContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.guild_config = None
        self.author_data = None
        if self.interaction.guild:
            self.guild_config = GuildConfig(self.interaction.guild.id)
            self.author_data = MemberData(self.interaction.user.id, self.interaction.guild.id)
    
    def translate(self, text_key: str, *args, **kwargs):
        if self.guild_config is None:
            return Lang.get_text(text_key, "en", *args, **kwargs)
        else:
            custom_translations = GuildLanguage(self.interaction.guild.id)
            return Lang.get_text(text_key, self.guild_config.language, custom_rows=custom_translations.rows, *args, **kwargs)
    
    async def translate_message(self, *args, **kwargs):
        text_key = kwargs.pop("text_key", None)
        text_args = kwargs.pop("text_args", {})
        if not text_key is None:
            translated_text = self.translate(text_key, **text_args)
            
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