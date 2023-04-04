from data_management import *

def get_article_names(self, ctx):
    return [f"{article.name} ({article._article_id})" for article in GuildArticle.list_articles(ctx.interaction.guild.id)]
def get_article_from_name(self, ctx, article_name) -> GuildArticle:
    article_id: int = int(article_name[article_name.rfind("(")+1:article_name.rfind(")")])
    return GuildArticle(article_id, ctx.guild.id)

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