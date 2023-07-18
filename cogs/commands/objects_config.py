from discord import *

from data_management import *
from utils.bot_autocompletes import *
from utils.bot_commands import *
from utils.bot_embeds import *
from utils.bot_views import *


class ObjectsConfigCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    objects = BotSlashCommandGroup("objects", default_member_permissions=Permissions(administrator=True), guild_only=True)
    change = objects.create_subgroup("change")

    @objects.command(name="create")
    @option("name", type=str, max_length=32, required=True)
    @option("description", type=str, max_length=1024, default="")
    async def create_object(self, ctx, name: str, description: str):
        new_object = GuildObject.new(ctx.guild.id, name)
        new_object.set_description(description)
        await ctx.respond(text_key="OBJECT_CREATED", text_args={"object": new_object.name})

    @change.command(name="name")
    @option("object", type=GuildObjectConverter, autocomplete=get_objects)
    @option("name", type=str, max_length=32)
    async def change_name(self, ctx, object: GuildObject, name: str):
        before_name = object.name
        object.set_name(name)
        await ctx.respond(text_key="OBJECT_NAME_CHANGED", text_args={"before": before_name, "after": name})
    
    @change.command(name="description")
    @option("object", type=GuildObjectConverter, autocomplete=get_objects)
    @option("description", type=str, max_length=1024)
    async def change_description(self, ctx, object: GuildObject, description: str):
        before_description = object.description
        object.set_description(description)
        await ctx.respond(text_key="OBJECT_DESCRIPTION_CHANGED", text_args={"before": before_description, "after": description})

    @change.command(name="refund")
    @option("object", type=GuildObjectConverter, autocomplete=get_objects)
    @option("is_refundable", type=bool)
    @option("refund_price", type=int)
    async def change_refund(self, ctx, object: GuildObject, is_refundable, refund_price):
        object.set_refundable(is_refundable, refund_price)
        if is_refundable:
            await ctx.respond(text_key="OBJECT_IS_REFUNDABLE", text_args={"object": object.name, "price": refund_price})
        else:
            await ctx.respond(text_key="OBJECT_IS_NOT_REFUNDABLE", text_args={"object": object.name})


    @objects.command(name="delete")
    @option("object", type=GuildObjectConverter, required=True, autocomplete=get_objects)
    async def delete_object(self, ctx, object: GuildObject):
        confirm_view = ConfirmView(ctx.author)
        confirm_embed = DangerEmbed(title=ctx.translate("DELETION"), description=ctx.translate("OBJECT_DELETION_CONFIRMATION", object=object.name))
        
        await ctx.respond(embed=confirm_embed, view=confirm_view)
        await confirm_view.wait()
        
        if confirm_view.confirmed:
            object.delete()
            await ctx.respond(text_key="OBJECT_DELETION_PERFORMED", text_args={"object": object.name})
        else:
            await ctx.respond(text_key="DELETION_CANCELLED")

    @objects.command(name="give")
    @default_permissions(administrator=True)
    @option("to", parameter_name="member", type=Member)
    @option("object", type=GuildObjectConverter, autocomplete=get_objects)
    @option("amount", type=int, default=1)
    async def give_object(self, ctx, member: Member, object: GuildObject, amount: int = 1):
        member_data = MemberData(member.id, ctx.guild.id)
        member_inventory = member_data.get_inventory()
        
        if member_inventory.is_full():
            await ctx.respond(text_key="INVENTORY_FULL", text_args={"member": member})
            return
            
        member_inventory.add_object(object, amount)
        member_data.set_inventory(member_inventory)

        await ctx.respond(text_key="OBJECT_GIVED", text_args={"object_name": object.name, "amount": amount, "member": member})

def setup(bot):
    bot.add_cog(ObjectsConfigCog(bot))