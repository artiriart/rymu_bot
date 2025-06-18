import discord
from discord.ext import commands
import psutil

class General(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Pong!")
    @discord.app_commands.describe() # Options basically
    async def hello_slash(self, interaction: discord.Interaction):
        user = interaction.user
        if user:
            await interaction.response.send_message(f"Pong!")
        else:
            await interaction.response.send_message(f"Hello, {interaction.user.display_name}!", ephemeral=True)



    @discord.app_commands.command(name="status", description="General Bot info")
    @discord.app_commands.describe()
    async def status_slash(self, interaction: discord.Interaction):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        embed = discord.Embed(
            title="Current Stats:",
            description=f"CPU Used: {cpu}%\n"
                        f"Mem Used: {mem.percent}%",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(General(bot))