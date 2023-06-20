from operator import attrgetter
from random import randint

from discord import *
from discord.ext.pages import Paginator

from data_management import *
from utils.bot_autocompletes import *
from utils.bot_commands import *
from utils.bot_embeds import *


class GlobalCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    about = BotSlashCommandGroup("about", guild_only=True)
    list_grp = BotSlashCommandGroup("list", guild_only=True)

    @about.command(name="object")
    @option("object", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    async def about_object(self, ctx, object: GuildObject):
        # articles = [article for article in GuildArticle.list_articles(ctx.guild.id) if article.has_object(object)]
        description = []
        for article in GuildArticle.list_articles(ctx.guild.id):
            if not article.has_object(object):
                continue
            
            quantity = article.get_quantity(object)
            if quantity <= 0:
                continue

            description.append(
                ctx.translate("WHERE_TO_BUY_TEMPLATE", article=article.name, unit_price=round(article.price/quantity, 2))
            )
        
        embed = NormalEmbed(title=object.name, description=object.description)
        if description:
            embed.add_field(name=ctx.translate("WHERE_TO_BUY"), value="\n".join(description))
        await ctx.respond(embed=embed)

    @about.command(name="article")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_articles)
    async def about_article(self, ctx, article: GuildArticle):
        embed = NormalEmbed(title=article.name, description=article.description or None)
        embed.add_field(name=ctx.translate("PRICE"), value=ctx.translate("ARTICLE_PRICE", price=article.price))

        roles = [ctx.guild.get_role(role_id).mention for role_id in article.role_ids]
        if roles != []:
            embed.add_field(name="Roles", value="\n".join(roles))
        
        objects = [GuildObject(object_id, ctx.guild.id) for object_id, amount in article.object_ids.items()]
        if objects != []:
            embed.add_field(name=ctx.translate("OBJECTS"), value="\n".join(f"{obj.name} | {article.get_quantity(obj)}" for obj in objects if obj)) #TODO: use a command instead of checking is object exists
        
        await ctx.respond(embed=embed)

    #TODO: for v4.1 search if there isn't a way to refactor all this code and not having the same code for 3 commands
    @list_grp.command(name="objects")
    async def list_objects(self, ctx):
        objects = GuildObject.list_objects(ctx.guild.id)
        sorted_objects = sorted(objects, key=attrgetter("_object_id"))

        embed_pages = []
        object_descriptions = []
        for i in range(len(sorted_objects)):
            obj = sorted_objects[i]
            object_descriptions.append(f"{obj.name} ({obj._object_id})")

            if (i+1) % 20 == 0 or i+1 == len(sorted_objects):
                embed = NormalEmbed(title=ctx.translate("OBJECTS"))
                embed.description = "\n".join(object_descriptions)
                embed_pages.append(embed)
                object_descriptions.clear()
        
        if embed_pages == []:
            embed = WarningEmbed(title=ctx.translate("NO_OBJECTS_EXISTS"))
            await ctx.respond(embed=embed)
            return
            
        paginator = Paginator(pages=embed_pages, show_disabled=False)
        await paginator.respond(ctx.interaction)

    @list_grp.command(name="articles")
    async def list_articles(self, ctx):
        articles = GuildArticle.list_articles(ctx.guild.id)
        sorted_articles = sorted(articles, key=attrgetter("_article_id"))

        embed_pages = []
        articles_description = []
        for i in range(len(sorted_articles)):
            article = sorted_articles[i]
            articles_description.append(f"{article.name} ({article._article_id})")

            if (i+1) % 20 == 0 or i+1 == len(sorted_articles):
                embed = NormalEmbed(title=ctx.translate("ARTICLES"))
                embed.description = "\n".join(articles_description)
                embed_pages.append(embed)
                articles_description.clear()
        
        if embed_pages == []:
            embed = WarningEmbed(title=ctx.translate("NO_ARTICLES_EXISTS"))
            await ctx.respond(embed=embed)
            return
        
        paginator = Paginator(pages=embed_pages, show_disabled=False)
        await paginator.respond(ctx.interaction)

    @list_grp.command(name="salaries")
    async def list_salaries(self, ctx):
        salaries = GuildSalaries(ctx.guild.id).salaries

        embeds = []
        description = []
        for i in range(len(salaries)):
            role_id = list(salaries.keys())[i]
            role = ctx.guild.get_role(int(role_id))
            pay = salaries[role_id]

            if not role is None:
                role = role.mention
            
            description.append(f"{role} : {pay}")
            if len(description) >= 20 or i+1 == len(salaries):
                embed = NormalEmbed(title="Salaries")
                embed.description = "\n".join(description)
                embeds.append(embed)
                description.clear()

        if embeds == []:
            embed = WarningEmbed(title=ctx.translate("NO_SALARIES_EXISTS"))
            await ctx.respond(embed=embed)
            return
            
        paginator = Paginator(pages=embeds, show_disabled=False)
        await paginator.respond(ctx.interaction)


    @bot_slash_command(name="profil")
    @guild_only()
    @option("member", type=Member, required=False, default=None)
    async def slash_profil(self, ctx, member = None):
        member = ctx.author if member == None else member
        await self.show_profil(ctx, member)
    
    @bot_user_command(name="profil")
    @guild_only()
    async def user_profil(self, ctx, member: Member):
        await self.show_profil(ctx, member, ephemeral=True)
    
    async def show_profil(self, ctx, member: Member, ephemeral=False):
        leveling_config = GuildLevelingConfig(ctx.guild.id)
        member_data = MemberData(member.id, ctx.guild.id)

        xp_goal = member_data.get_xp_goal(leveling_config.formula)
        embed = NormalEmbed(title=ctx.translate("PROFIL_OF", member=member))
        embed.add_field(name=ctx.translate("LEVEL_NAME"), value=str(member_data.level))
        embed.add_field(name=ctx.translate("XP_NAME"), value=f"{member_data.xp}/{xp_goal}")
        embed.add_field(name=ctx.translate("MONEY_NAME"), value=str(member_data.money))
        
        await ctx.respond(embed=embed, ephemeral=ephemeral)
        
    @bot_user_command(name="inventory")
    @guild_only()
    async def user_show_inventory(self, ctx, member: Member):
        await self.show_inventory(ctx, member, ephemeral=True)

    @bot_slash_command(name="inventory")
    @option("member", type=Member, required=False)
    async def slash_show_inventory(self, ctx, member=None):
        member = ctx.author if member == None else member
        await self.show_inventory(ctx, member)
    
    async def show_inventory(self, ctx, member, ephemeral=False):
        member_data = MemberData(member.id, ctx.guild.id)

        inventory = member_data.get_inventory()
        object_ids = inventory.get_object_ids()
        player_objects = {GuildObject(object_id, ctx.guild.id): inventory.get_object_amount(object_id) for object_id in object_ids} # dict {object: quantity of that object}
        if None in player_objects: player_objects.pop(None)
        
        description = "\n".join(f"{obj.name} | {player_objects[obj]}" for obj in player_objects) or ctx.translate("INVENTORY_EMPTY")

        embed = NormalEmbed(title=ctx.translate("INVENTORY_OF", member=member))
        embed.description = description

        await ctx.respond(embed=embed, ephemeral=ephemeral)

    # @bot_slash_command(name="sell") # TODO: v4.1
    # async def sell(self, ctx):
    #     await ctx.respond("sell object")


    @bot_slash_command(name="buy")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_articles)
    # @option("quantity", type=int, default=1, max_value=999, required=False) #TODO: Can buy more than one bypassing cooldown
    @guild_only()
    async def buy_article(self, ctx, article: GuildArticle, quantity: int = 1):
        print("by")
        if quantity <= 0:
            await ctx.respond("????") # Wtf are you trying to bug????
            return

        await article.buy(ctx, quantity)
        await ctx.respond(text_key="ARTICLE_PURCHASED", text_args={"article": article.name})

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot: # Ignore bots
            return
        if message.guild is None: # Ignore non guild origin
            return

        ctx = await self.bot.get_context(message)
        is_command = not ctx.command is None

        if self.bot.user in message.mentions:
            if randint(0, 99) == 0: # Little easteregg lol
                await message.reply("Yo, it's me")
            if len(message.raw_mentions) == 1 and message.content == f"<@{message.raw_mentions[0]}>":
                # The message only mention the bot
                # await message.reply("Stats")
                pass

        leveling_config = GuildLevelingConfig(ctx.guild.id)
        author_is_banned = leveling_config.is_member_ban(message.author)
        channel_is_banned = leveling_config.is_channel_ban(ctx.channel)
        if leveling_config.enabled and not (is_command or author_is_banned or channel_is_banned):
            # Add xp to author
            level_before = ctx.author_data.level
            ctx.author_data.add_xp(int(len(message.content) / 10 + 1))
            level_after = ctx.author_data.refresh_level(leveling_config.formula)

            if level_before < level_after:
                await ctx.send(leveling_config.send_message(ctx.author, level_before, level_after))
                ctx.author_data.add_money(randint(*sorted([leveling_config.min_gain, leveling_config.max_gain])))

def setup(bot):
    bot.add_cog(GlobalCog(bot))