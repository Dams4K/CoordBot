import discord
import json
from discord.ext import commands
from discord.ui import Modal, InputText
from data_management import GuildConfig
from utils.references import References
from utils.bot_embeds import NormalEmbed, DangerEmbed

def get_suggests_channel(bot):
    return bot.get_channel(References.SUGGESTS_CHANNEL_ID)
def get_reports_channel(bot):
    return bot.get_channel(References.REPORTS_CHANNEL_ID)


class SuggestModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Suggest Modal")

        self.bot = bot
        self.add_item(InputText(label="Name", style=discord.InputTextStyle.singleline, max_length=256))
        self.add_item(InputText(label="Développement", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_suggests_channel(self.bot)
        embed = NormalEmbed(GuildConfig(interaction.guild_id), title=self.children[0].value, description=self.children[1].value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        await channel.send(embed=embed, view=ResponseSender(self.bot))
        await interaction.response.send_message("Suggestion envoyé", ephemeral=True)


class ReportModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Report Modal")
        self.bot = bot
        self.add_item(InputText(label="Explication du bug", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_reports_channel(self.bot)
        embed = DangerEmbed(GuildConfig(interaction.guild_id), title="Report", description=self.children[0].value)
        embed.set_footer(text=f"{interaction.user.id}, {interaction.channel_id}")

        await channel.send(embed=embed, view=ResponseSender(self.bot))
        await interaction.response.send_message("Report envoyé", ephemeral=True)


class ResponseModal(discord.ui.Modal):
    def __init__(self, bot, user, channel, response_channel_origin):
        super().__init__(title="Response Menu")
        self.bot = bot
        self.user = user
        self.channel = channel
        self.response_channel_origin = response_channel_origin

        self.add_item(InputText(label="Response", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        response = self.children[0].value

        await interaction.response.send_message(response)
        response_message = await interaction.original_response()

        embed = NormalEmbed(GuildConfig(interaction.guild_id), title=f"Réponse", description="Tu as reçu une réponse de la part du développeur pour ta suggestion")
        embed.set_footer(text=f"{self.response_channel_origin}, {response_message.id}")
        await self.channel.send(self.user.mention, embed=embed, view=ResponseViewer(self.bot))


class ResponseSender(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="Respond", custom_id="respond-button", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        response_embed = interaction.message.embeds[0]
        author_id, channel_id = response_embed.footer.text.split(",")

        user = self.bot.get_user(int(author_id))
        channel = self.bot.get_channel(int(channel_id))
        
        if user == None or channel == None: return

        await interaction.response.send_modal(ResponseModal(self.bot, user, channel, interaction.channel_id))


class ResponseViewer(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="See response", custom_id="see-response", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        member_mention = interaction.message.content

        author_id = member_mention[member_mention.find("<@")+2:member_mention.find(">")]
        if author_id.isnumeric() and int(author_id) == interaction.user.id:
            response_embed = interaction.message.embeds[0]
            channel_id, message_id = response_embed.footer.text.split(",")

            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            embed = NormalEmbed(GuildConfig(interaction.guild_id), title="Réponse du développeur", description=message.content)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = DangerEmbed(GuildConfig(interaction.guild_id), title="Erreur", description="Vous n'êtes pas autorisé à lire la réponse")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ResponseSender(self.bot))
        self.bot.add_view(ResponseViewer(self.bot))

    @commands.slash_command(name="suggest")
    async def suggest(self, ctx):
        await ctx.send_modal(SuggestModal(self.bot))
    
    @commands.slash_command(name="reports")
    async def report(self, ctx):
        await ctx.send_modal(ReportModal(self.bot))


def setup(bot):
    bot.add_cog(DevTools(bot))