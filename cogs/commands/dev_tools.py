import discord
import json
from discord.ext import commands
from discord.ui import Modal, InputText

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ResponseSender(self.bot))

    @commands.slash_command(name="suggest")
    async def suggest(self, ctx):
        await ctx.send_modal(SuggestModal(self.bot))


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

        await interaction.response.send_modal(ResponseModal(user, channel))
class ResponseViewer(discord.ui.View):
    @discord.ui.button(label="See response", custom_id="see-response", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("qsdoqsdjhqsjhdqs", ephemeral=True)



class ResponseModal(discord.ui.Modal):
    def __init__(self, user, channel):
        super().__init__(title="Response Menu")
        self.user = user
        self.channel = channel

        self.add_item(InputText(label="Response", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        embed = discord.Embed(title="Réponse", description=f"Tu as reçu une réponse de la part du développeur")
        await self.channel.send(self.user.mention, embed=embed, view=ResponseViewer())
        await interaction.response.send_message("Réponse envoyé", ephemeral=True)
class SuggestModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Suggest Menu")

        self.bot = bot
        self.add_item(InputText(label="Name", style=discord.InputTextStyle.singleline, max_length=256))
        self.add_item(InputText(label="Développement", style=discord.InputTextStyle.paragraph))
    
    async def callback(self, interaction):
        channel = self.bot.get_channel(892459727240433706)
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value)

        infos = {
            "author_id": interaction.user.id,
            "channel_id": interaction.channel_id
        }

        await channel.send(content=str(infos), embed=embed, view=ResponseSender(self.bot))
        await interaction.response.send_message("Suggestion envoyé", ephemeral=True)


def setup(bot):
    bot.add_cog(DevTools(bot))