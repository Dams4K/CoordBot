from data_management import *

def get_articles(self, ctx):
    guild_id = ctx.interaction.guild.id
    article_names = [article.name for article in GuildArticle.list_articles(guild_id)]

    result = []
    for article in GuildArticle.list_articles(guild_id):
        if not article.name.startswith(ctx.value):
            continue

        formatted = article.name
        if article_names.count(article.name) > 1:
            formatted += f" ({article._article_id})"
        result.append(formatted)

    return result

#TODO: optimised
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