import datetime
from importlib.metadata import version
from random import randint

from discord import *
from discord.ext.pages import Paginator

from data_management import *
from utils.bot_autocompletes import *
from utils.bot_commands import *
from utils.bot_embeds import *
from utils.references import References

class BasicCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    about = BotSlashCommandGroup("about", guild_only=True)
    list = BotSlashCommandGroup("list", guild_only=True)

    @about.command(name="object")
    @option("object", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    async def about_object(self, ctx, object: GuildObject):
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
        embed.set_footer(text=f"id: {object._object_id}")
        await ctx.respond(embed=embed)

    @about.command(name="article")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_articles)
    async def about_article(self, ctx, article: GuildArticle):
        embed = NormalEmbed(title=article.name, description=article.description or None)
        embed.add_field(name=ctx.translate("PRICE"), value=ctx.translate("ARTICLE_PRICE", price=article.price))

        # Add roles
        if roles := await article.fetch_roles(ctx.guild):
            embed.add_field(name="Roles", value="\n".join([role.mention for role in roles]))
        
        # Add objetcs
        objects = [GuildObject(object_id, ctx.guild.id) for object_id, amount in article.object_ids.items()]
        if objects != []:
            embed.add_field(name=ctx.translate("OBJECTS"), value="\n".join(f"{obj.name} | {article.get_quantity(obj)}" for obj in objects if obj)) #TODO: use a command instead of checking is object exists
        
        # Show cooldown
        if article.cooldown > 0:
            embed.set_footer(text=f"Cooldown: {datetime.timedelta(seconds=article.cooldown)} | id: {article._article_id}")

        await ctx.respond(embed=embed)

    #TODO: for v4.1 search if there isn't a way to refactor all this code and not having the same code for 3 commands
    @list.command(name="objects")
    async def list_objects(self, ctx):
        objects = GuildObject.list_objects(ctx.guild.id)
        object_names = [obj.name for obj in objects]

        embed_pages = []
        object_descriptions = []
        page_size = 20

        for i, obj in enumerate(objects, 1):
            if object_names.count(obj.name) > 1:
                object_descriptions.append(f"{obj.name} ({obj._object_id})")
            else:
                object_descriptions.append(f"{obj.name}")

            if i % page_size == 0 or i == len(object_names):
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

    @list.command(name="articles")
    async def list_articles(self, ctx):
        articles = GuildArticle.list_articles(ctx.guild.id)
        article_names = [article.name for article in articles]

        embed_pages = []
        articles_description = []
        page_size = 20
        
        for i, article in enumerate(articles, 1):
            if article_names.count(article.name) > 1:
                articles_description.append(f"{article.name} ({article._article_id}): **{article.price}" + ctx.translate("MONEY_NAME:casefold")[0] + "**")
            else:
                articles_description.append(f"{article.name}: **{article.price}" + ctx.translate("MONEY_NAME:casefold")[0] + "**")

            if i % page_size == 0 or i == len(article_names):
                embed = NormalEmbed(title=ctx.translate("ARTICLES"))
                embed.description = "\n".join(articles_description)
                embed_pages.append(embed)
                articles_description.clear()

        if embed_pages == []:
            embed = WarningEmbed(title=ctx.translate("NO_ARTICLES_EXISTS"))
            await ctx.respond(embed=embed)
        else:
            paginator = Paginator(pages=embed_pages, show_disabled=False)
            await paginator.respond(ctx.interaction)

    @list.command(name="salaries")
    async def list_salaries(self, ctx):
        salaries: tuple = await (GuildSalaries(ctx.guild.id).fetch_salaries(ctx.guild)) # ([roles], [pays])

        footer_text = ctx.translate("SALARIES_PAYMENT_DATE")
        embeds = []
        description = []
        page_size = 20
        
        for i, (role, pay) in enumerate(zip(*salaries), 1):
            description.append(f"{role.mention} : {pay}")
            if i % page_size == 0 or i == len(salaries[0]):
                embed = NormalEmbed(title="Salaries")
                embed.set_footer(text=footer_text)
                embed.description = "\n".join(description)
                embeds.append(embed)
                description.clear()
        
        if embeds == []:
            embed = WarningEmbed(title=ctx.translate("NO_SALARIES_EXISTS"))
            embed.set_footer(text=footer_text)
            await ctx.respond(embed=embed)
            return

        paginator = Paginator(pages=embeds, show_disabled=False)
        await paginator.respond(ctx.interaction)


    @bot_slash_command(name="profil")
    @guild_only()
    @option("of", type=Member, required=False, default=None)
    async def slash_profil(self, ctx, of = None):
        member = ctx.author if of == None else of
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
    @guild_only()
    @option("of", type=Member, required=False)
    async def slash_show_inventory(self, ctx, of=None):
        member = ctx.author if of == None else of
        await self.show_inventory(ctx, member)
    
    async def show_inventory(self, ctx, member, ephemeral=False):
        member_data = MemberData(member.id, ctx.guild.id)

        inventory = member_data.get_inventory()
        object_ids = inventory.get_object_ids()
        player_objects = {GuildObject(object_id, ctx.guild.id): inventory.get_object_amount(object_id) for object_id in object_ids} # dict {object: quantity of that object}
        if None in player_objects: player_objects.pop(None)
        
        description: list = []
        for object, amount in player_objects.items():
            if amount > 1:
                description.append(f"{object.name} x{amount}")
            else:
                description.append(f"{object.name}")

        embed = NormalEmbed(title=ctx.translate("INVENTORY_OF", member=member))
        embed.description = "\n".join(description) or ctx.translate("INVENTORY_EMPTY")

        await ctx.respond(embed=embed, ephemeral=ephemeral)

    # @bot_slash_command(name="sell") # TODO: v4.1
    # async def sell(self, ctx):
    #     await ctx.respond("sell object")


    @bot_slash_command(name="buy")
    @option("article", type=GuildArticleConverter, required=True, autocomplete=get_articles)
    # @option("quantity", type=int, default=1, max_value=999, required=False) #TODO: Can buy more than one bypassing cooldown
    @guild_only()
    async def buy_article(self, ctx, article: GuildArticle, quantity: int = 1):
        if quantity <= 0:
            await ctx.respond("????") # Wtf are you trying to buy????
            return

        quantity = await article.buy(ctx, quantity)
        if quantity == 1:
            await ctx.respond(text_key="ARTICLE_PURCHASED", text_args={"article": article.name})
        else:
            await ctx.respond(text_key="ARTICLE_PURCHASED_X_TIMES", text_args={"article": article.name, "quantity": quantity})

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
            if self.bot.user.mention == message.content:
                app_info = await self.bot.application_info()
                team = app_info.team
                developers = team.members if team else [app_info.owner]
                bot_version = f"v{References.VERSION}" # TODO (idea): add "-dev" when we are using a non released version


                embed = InformativeEmbed(title=ctx.translate("ABOUT_BOT"))
                embed.add_field(name="Py-cord", value=f"v{version('py-cord')}")
                embed.add_field(name=self.bot.user.display_name, value=bot_version, inline=False)
                if len(developers) > 1:
                    embed.add_field(name=ctx.translate("BOT_DEVELOPERS"), value="\n".join(f"`{developer.name}`" for developer in developers))
                elif len(developers) == 1:
                    embed.add_field(name=ctx.translate("BOT_DEVELOPER"), value=f"{developers[0].name}")
                await message.reply(embed=embed)

        leveling_config = GuildLevelingConfig(ctx.guild.id)
        author_is_banned = leveling_config.is_member_ban(message.author)
        channel_is_banned = leveling_config.is_channel_ban(ctx.channel)
        if leveling_config.enabled and not (is_command or author_is_banned or channel_is_banned):
            # Add xp to author
            level_before = ctx.author_data.level
            ctx.author_data.add_xp(int(len(message.content) / 10 + 1))
            level_after = ctx.author_data.refresh_level(leveling_config.formula)

            if level_before < level_after:
                earned_money = randint(*sorted([leveling_config.min_gain, leveling_config.max_gain]))
                ctx.author_data.add_money(earned_money)

                if m := leveling_config.get_message(member=ctx.author, level_before=level_before, level_after=level_after, earned_money=earned_money):
                    # Send message only if it's not empty
                    await ctx.send(m)

def setup(bot):
    bot.add_cog(BasicCog(bot))