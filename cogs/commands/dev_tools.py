import discord
import json
from discord.ext import commands
from discord.ui import Modal, InputText
from utils.references import References
from utils.bot_embeds import NormalEmbed, DangerEmbed

def get_suggests_channel(bot):
    return bot.get_channel(References.SUGGESTS_CHANNEL_ID)

class ResponseModal(discord.ui.Modal):
    def __init__(self, bot, user, channel):
        super().__init__(title="Response Menu")
        self.bot = bot
        self.user = user
        self.channel = channel

        self.add_item(InputText(label="Response", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        response = self.children[0].value

        suggests_channel = get_suggests_channel(self.bot)
        response_message = await suggests_channel.send(response)

        embed = discord.Embed(title=f"Réponse ({response_message.id})", description="Tu as reçu une réponse de la part du développeur pour ta suggestion")
        await self.channel.send(self.user.mention, embed=embed, view=ResponseViewer(self.bot))
        await interaction.response.send_message("Réponse envoyé", ephemeral=True)
    

class SuggestModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Suggest Menu")

        self.bot = bot
        self.add_item(InputText(label="Name", style=discord.InputTextStyle.singleline, max_length=256))
        self.add_item(InputText(label="Développement", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = get_suggests_channel(self.bot)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value)

        infos = {
            "author_id": interaction.user.id,
            "channel_id": interaction.channel_id
        }

        await channel.send(content=str(infos), embed=embed, view=ResponseSender(self.bot))
        await interaction.response.send_message("Suggestion envoyé", ephemeral=True)


class ResponseSender(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @discord.ui.button(label="Respond", custom_id="respond-button", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        infos = json.loads(interaction.message.content.replace("'", '"'))
        author_id = int(infos["author_id"])
        channel_id = int(infos["channel_id"])
        
        user = self.bot.get_user(author_id)
        channel = self.bot.get_channel(channel_id)
        
        if user == None or channel == None: return

        await interaction.response.send_modal(ResponseModal(self.bot, user, channel))


class ResponseViewer(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="See response", custom_id="see-response", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        member_mention = interaction.message.content
        response_embed = interaction.message.embeds[0]
        title = response_embed.title

        author_id = member_mention[member_mention.find("<@")+2:member_mention.find(">")]
        if author_id.isnumeric() and int(author_id) == interaction.user.id:
            message_id = title[title.find("(")+1:title.find(")")]

            suggests_channel = get_suggests_channel(self.bot)
            message = await suggests_channel.fetch_message(message_id)

            # embed = NormalEmbed(interaction, title="Réponse du développeur", description=message.content)
            await interaction.response.send_message(message.content, ephemeral=True)
        else:
            # embed = DangerEmbed(interaction, title="Erreur", description="Vous n'êtes pas autorisé à lire la réponse")
            await interaction.response.send_message("Vous n'êtes pas autorisé à lire la réponse", ephemeral=True)


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


def setup(bot):
    bot.add_cog(DevTools(bot))