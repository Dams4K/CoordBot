from data_management import *

def get_article_names(self, ctx):
    return [f"{article.name} ({article._article_id})" for article in GuildArticle.list_articles(ctx.interaction.guild.id)]
def get_article_from_name(self, ctx, article_name) -> GuildArticle:
    article_id: int = int(article_name[article_name.rfind("(")+1:article_name.rfind(")")])
    return GuildArticle(article_id, ctx.guild.id)

#TODO: optimised
def get_items(self, ctx):
    guild_id = ctx.interaction.guild.id
    item_names = [item.name for item in GuildItem.list_items(guild_id)]

    result = []
    for item in GuildItem.list_items(guild_id):
        if not item.name.startswith(ctx.value):
            continue

        formatted = item.name
        if item_names.count(item.name) > 1:
            formatted += f" ({item._item_id})"
        result.append(formatted)

    return result