import discord
import json
from discord.ext import commands
from discord.ext import bridge
from discord.ui import Modal, InputText
from data_management import GuildConfig
from lang.lang import Lang
from utils.references import References
from utils.bot_embeds import NormalEmbed, DangerEmbed
from utils.bot_contexts import *

def get_suggests_channel(bot):
    return bot.get_channel(References.SUGGESTS_CHANNEL_ID)
def get_reports_channel(bot):
    return bot.get_channel(References.REPORTS_CHANNEL_ID)


class SuggestModal(discord.ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext):
        super().__init__(title=ctx.translate("SUGGEST_MODAL"))

        self.bot = bot
        self.ctx = ctx
        self.add_item(InputText(label=ctx.translate("SUGGEST_NAME"), style=discord.InputTextStyle.singleline, max_length=256, required=False))
        self.add_item(InputText(label=ctx.translate("SUGGEST_EXPLANATION"), style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_suggests_channel(self.bot)
        embed = NormalEmbed(GuildConfig(interaction.guild_id), title=f"- {self.children[0].value} -", description=self.children[1].value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        await channel.send(embed=embed, view=ResponseSender(self.bot, self.ctx))
        await interaction.response.send_message(self.ctx.translate("SUGGEST_SENT"), ephemeral=True)


class ReportModal(discord.ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext):
        super().__init__(title=ctx.translate("REPORT_MODAL"))
        self.bot = bot
        self.ctx = ctx
        self.add_item(InputText(label=ctx.translate("REPORT_EXPLANATION"), style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_reports_channel(self.bot)
        embed = DangerEmbed(GuildConfig(interaction.guild_id), title=self.ctx.translate("NEW_REPORT"), description=self.children[0].value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        await channel.send(embed=embed, view=ResponseSender(self.bot, self.ctx))
        await interaction.response.send_message(self.ctx.translate("REPORT_SENT"), ephemeral=True)


class ResponseModal(discord.ui.Modal):
    def __init__(self, bot, ctx: BotBridgeContext, user, channel, response_channel_origin):
        super().__init__(title=ctx.translate("RESPONSE_MENU"))
        self.bot = bot
        self.ctx = ctx
        self.user = user
        self.channel = channel
        self.response_channel_origin = response_channel_origin

        self.add_item(InputText(label=ctx.translate("RESPONSE"), style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        response = self.children[0].value

        await interaction.response.send_message(response)
        response_message = await interaction.original_response()

        response_receive_text = self.ctx.translate("SUGGEST_RESPONSE_RECEIVED") if self.channel.id == References.SUGGESTS_CHANNEL_ID else self.ctx.translate("REPORT_RESPONSE_RECEIVED")
        embed = NormalEmbed(GuildConfig(interaction.guild_id), title=self.ctx.translate("RESPONSE"), description=response_receive_text)
        embed.set_footer(text=f"{self.response_channel_origin}, {response_message.id}")
        await self.channel.send(self.user.mention, embed=embed, view=ResponseViewer(self.bot, self.ctx))


class ResponseSender(discord.ui.View):
    def __init__(self, bot, ctx: BotBridgeContext = None):
        super().__init__(timeout=None)
        self.bot = bot

        if ctx is not None:
            for child in self.children:
                child.label = ctx.translate(child.label)
    
    @discord.ui.button(label="RESPOND", custom_id="respond-button", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        ctx = await self.bot.get_context(interaction.message)
        response_embed = interaction.message.embeds[0]
        author_id, channel_id = response_embed.footer.text.split(",")

        user = self.bot.get_user(int(author_id))
        channel = self.bot.get_channel(int(channel_id))
        
        if user == None or channel == None: return

        await interaction.response.send_modal(ResponseModal(self.bot, ctx, user, channel, interaction.channel_id))


class ResponseViewer(discord.ui.View):
    def __init__(self, bot, ctx: BotBridgeContext = None):
        self.bot = bot
        super().__init__(timeout=None)

        if ctx is not None:
            for child in self.children:
                child.label = ctx.translate(child.label)

    @discord.ui.button(label="SEE_RESPONSE", custom_id="see-response", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        ctx = await self.bot.get_context(interaction.message)
        member_mention = interaction.message.content

        author_id = member_mention[member_mention.find("<@")+2:member_mention.find(">")]
        if author_id.isnumeric() and int(author_id) == interaction.user.id:
            response_embed = interaction.message.embeds[0]
            channel_id, message_id = response_embed.footer.text.split(",")

            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            embed = NormalEmbed(GuildConfig(interaction.guild_id), title=ctx.translate("DEVELOPER_RESPONSE"), description=message.content)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = DangerEmbed(GuildConfig(interaction.guild_id), title="Erreur", description=ctx.translate("NOT_ALLOW_SEE_RESPONSE"))
            await interaction.response.send_message(embed=embed, ephemeral=True)


class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ResponseSender(self.bot))
        self.bot.add_view(ResponseViewer(self.bot))

    @bridge.bridge_command(name="suggest")
    async def suggest(self, ctx):
        await ctx.send_modal(SuggestModal(self.bot, ctx))
    
    @bridge.bridge_command(name="report")
    async def report(self, ctx):
        await ctx.send_modal(ReportModal(self.bot, ctx))


def setup(bot):
    bot.add_cog(DevTools(bot))