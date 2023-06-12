import json
from discord import *
from data_management import GuildConfig
from lang.lang import Lang
from utils.references import References
from utils.bot_embeds import *
from utils.bot_contexts import *
from utils.bot_commands import bot_slash_command, bot_message_command

def get_suggests_channel(bot):
    return bot.get_channel(References.SUGGESTS_CHANNEL_ID)
def get_reports_channel(bot):
    return bot.get_channel(References.REPORTS_CHANNEL_ID)


class SuggestModal(ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext):
        super().__init__(title=ctx.translate("SUGGEST_MODAL"))

        self.bot = bot
        self.ctx = ctx
        self.add_item(ui.InputText(label=ctx.translate("SUGGEST_NAME"), style=InputTextStyle.singleline, max_length=256, required=False))
        self.add_item(ui.InputText(label=ctx.translate("SUGGEST_EXPLANATION"), style=InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_suggests_channel(self.bot)
        embed = NormalEmbed(title=f"- {self.children[0].value} -", description=self.children[1].value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        await channel.send(embed=embed, view=ResponseSender(self.bot, self.ctx))
        await interaction.response.send_message(self.ctx.translate("SUGGEST_SENT"), ephemeral=True)


class ReportModal(ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext, attached_message: Message = None):
        super().__init__(title=ctx.translate("REPORT_MODAL"))
        self.bot = bot
        self.ctx = ctx

        attached_message_id = attached_message.id if attached_message else ""

        self.attached_message_id_input = ui.InputText(label=ctx.translate("ATTACHED_MESSAGE_ID"), style=InputTextStyle.short, placeholder=bot.user.id, value=attached_message_id)
        self.message_input = ui.InputText(label=ctx.translate("REPORT_EXPLANATION"), style=InputTextStyle.paragraph)

        self.add_item(self.attached_message_id_input)
        self.add_item(self.message_input)
    
    async def callback(self, interaction):
        guild = interaction.guild

        channel = get_reports_channel(self.bot)
        embed = DangerEmbed(title=self.ctx.translate("NEW_REPORT"), description=self.message_input.value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        attached_message = None

        attached_message_id = self.attached_message_id_input.value
        if attached_message_id.isnumeric():
            try:
                attached_message = await self.ctx.channel.fetch_message(int(attached_message_id))
            except NotFound:
                not_found_embed = DangerEmbed(title=self.ctx.translate("WARNING"), description=self.ctx.translate("MESSAGE_NOT_FOUND"))

                await interaction.response.send_message(embeds=[not_found_embed, self.get_failed_to_sent_embed()], ephemeral=True)
                return
            except Forbidden:
                forbidden_embed = DangerEmbed(title=self.ctx.translate("WARNING"), description=self.ctx.translate("ACCESS_FORBIDDEN"))

                await interaction.response.send_message(embeds=[forbidden_embed, self.get_failed_to_sent_embed()], ephemeral=True)
                return
            else:
                if attached_message.author.id not in [self.ctx.author.id, self.bot.user.id]:
                    not_your_message_embed = DangerEmbed(title=self.ctx.translate("WARNING"), description=self.ctx.translate("REPORT_ATTACHED_MESSAGE_CONDITIONS"))

                    await interaction.response.send_message(embeds=[not_your_message_embed, self.get_failed_to_sent_embed()], ephemeral=True)
                    return
 
        
        msg = await channel.send(embed=embed, view=ResponseSender(self.bot, self.ctx))

        if attached_message is not None:
            files = [await attachement.to_file() for attachement in attached_message.attachments]
            await msg.reply(attached_message.content, embeds=attached_message.embeds, files=files)

        await interaction.response.send_message(self.ctx.translate("REPORT_SENT"), ephemeral=True)

    def get_failed_to_sent_embed(self):
        embed = DangerEmbed(title=self.ctx.translate("REPORT_MESSAGE_NOT_SENT"), description=self.message_input.value)
        return embed


class ResponseModal(ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext, user, channel, response_channel_origin):
        super().__init__(title=ctx.translate("RESPONSE_MENU"))
        self.bot = bot
        self.ctx = ctx
        self.user = user
        self.channel = channel
        self.response_channel_origin = response_channel_origin

        self.add_item(ui.InputText(label=ctx.translate("RESPONSE"), style=InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        response = self.children[0].value

        await interaction.response.send_message(response)
        response_message = await interaction.original_response()

        response_receive_text = self.ctx.translate("SUGGEST_RESPONSE_RECEIVED") if self.channel.id == References.SUGGESTS_CHANNEL_ID else self.ctx.translate("REPORT_RESPONSE_RECEIVED")
        embed = NormalEmbed(title=self.ctx.translate("RESPONSE"), description=response_receive_text)
        embed.set_footer(text=f"{self.response_channel_origin}, {response_message.id}")
        await self.channel.send(self.user.mention, embed=embed, view=ResponseViewer(self.bot, self.ctx))


class ResponseSender(ui.View):
    def __init__(self, bot, ctx: BotBridgeContext = None):
        super().__init__(timeout=None)
        self.bot = bot

        if ctx is not None:
            for child in self.children:
                child.label = ctx.translate(child.label)
    
    @ui.button(label="RESPOND", custom_id="respond-button", style=ButtonStyle.green)
    async def button_callback(self, button, interaction):
        ctx = await self.bot.get_context(interaction.message)
        response_embed = interaction.message.embeds[0]
        author_id, channel_id = response_embed.footer.text.split(",")

        user = self.bot.get_user(int(author_id))
        channel = self.bot.get_channel(int(channel_id))
        
        if user == None or channel == None: return

        await interaction.response.send_modal(ResponseModal(self.bot, ctx, user, channel, interaction.channel_id))


class ResponseViewer(ui.View):
    def __init__(self, bot, ctx: BotBridgeContext = None):
        self.bot = bot
        super().__init__(timeout=None)

        if ctx is not None:
            for child in self.children:
                child.label = ctx.translate(child.label)

    @ui.button(label="SEE_RESPONSE", custom_id="see-response", style=ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        ctx = await self.bot.get_context(interaction.message)
        member_mention = interaction.message.content

        author_id = member_mention[member_mention.find("<@")+2:member_mention.find(">")]
        if author_id.isnumeric() and int(author_id) == interaction.user.id:
            response_embed = interaction.message.embeds[0]
            channel_id, message_id = response_embed.footer.text.split(",")

            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            embed = NormalEmbed(title=ctx.translate("DEVELOPER_RESPONSE"), description=message.content)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = DangerEmbed(title="Erreur", description=ctx.translate("NOT_ALLOW_SEE_RESPONSE"))
            await interaction.response.send_message(embed=embed, ephemeral=True)


class DevTools(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ResponseSender(self.bot))
        self.bot.add_view(ResponseViewer(self.bot))

    @bot_message_command(name="Bug report")
    async def message_report(self, ctx, message):
        if message.author.id not in [ctx.author.id, self.bot.user.id]:
            not_your_message_embed = DangerEmbed(title=ctx.translate("WARNING"), description=ctx.translate("REPORT_ATTACHED_MESSAGE_CONDITIONS"))

            await ctx.respond(embed=not_your_message_embed, ephemeral=True)
            return
        
        await ctx.send_modal(ReportModal(self.bot, ctx, attached_message=message))

    @bot_slash_command(name="report")
    async def report(self, ctx):
        await ctx.send_modal(ReportModal(self.bot, ctx))
    
    @bot_slash_command(name="suggest")
    async def suggest(self, ctx):
        await ctx.send_modal(SuggestModal(self.bot, ctx))
    


def setup(bot):
    bot.add_cog(DevTools(bot))