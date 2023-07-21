from data_management import *

def get_articles(self, ctx):
    guild_id = ctx.interaction.guild.id
    article_names = [article.name for article in GuildArticle.list_articles(guild_id)]

    result = []
    for article in GuildArticle.list_articles(guild_id):
        # We only want articles that start with what the user has written
        if not article.name.lower().startswith(ctx.value.lower()):
            continue

        formatted = article.name
        if article_names.count(article.name) > 1:
            formatted += f" ({article._article_id})"
        result.append(formatted)

    return result

#TODO: optimize
def get_objects(self, ctx):
    guild_id = ctx.interaction.guild.id
    object_names = [obj.name for obj in GuildObject.list_objects(guild_id)]

    result = []
    for obj in GuildObject.list_objects(guild_id):
        if not obj.name.startswith(ctx.value):
            continue

        formatted = obj.name
        if object_names.count(obj.name) > 1:
            formatted += f" ({obj._object_id})"
        result.append(formatted)

    return result

def get_languages(self, ctx):
    return [Lang.get_text("CHANGE_LANGUAGE_TO", lang) for lang in Lang.get_languages() if lang.startswith(ctx.value)]

def get_translation_keys(self, ctx):
    return [key for key in Lang.get_keys() if key.startswith(ctx.value)]

async def get_custom_translations(self, ctx):
    guild_language = GuildLanguage(ctx.interaction.guild.id)
    return [key for key in guild_language.get_keys() if key.startswith(ctx.value)]
