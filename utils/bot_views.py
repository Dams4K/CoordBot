import discord

class ConfirmView(discord.ui.View):
    def __init__(self, author: discord.Member):
        super().__init__()
        self.author = None
        if isinstance(author, discord.Member) and author:
            self.author = author

        self.confirmed = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.author and interaction.user.id != self.author.id:
            return

        await interaction.response.send_message("Confirming", ephemeral=True)
        self.confirmed = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.author and interaction.user.id != self.author.id:
            return
        
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.confirmed = False
        self.stop()