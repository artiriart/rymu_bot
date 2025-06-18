from discord.ext import commands
import discord
import sqlite3

class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions = {}

    async def mining_interaction(self, user: discord.User, use_menu: bool):
        mana = self.active_sessions[user.id].get("mana", 0)
        embed = discord.Embed(
            description="# Mining Simulator",
            color=self.active_sessions[user.id].get("embed_color", discord.Color.random())
        )
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.set_footer(text=f"Your Mana: {mana}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="Mine", emoji="⛏️", custom_id=f"mine-{user.id}"))
        if mana >= 20:
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.success, label="Blast", emoji="💣", custom_id=f"blast-{user.id}"))
        else:
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="Blast (20 Mana)", emoji="💣",custom_id="x", disabled=True))
        return embed, view

    @discord.app_commands.command(name="mine", description="Start a Mining Session")
    @discord.app_commands.describe(use_menu="Use Special Items?") # Options basically
    async def  mine_slash(self, interaction: discord.Interaction, use_menu:bool):
        if interaction.user.id in self.active_sessions:
            await interaction.response.send_message("You already have an active mining session!", ephemeral=True)
            return
        self.active_sessions[interaction.user.id] = {"mana":0, "embed_color":discord.Color.random()}
        embed, view = await self.mining_interaction(interaction.user, use_menu)
        await interaction.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data.get("custom_id", "")
            user_id = interaction.user.id
            if custom_id.startswith("mine"):
                if custom_id == f"mine-{user_id}":
                    self.active_sessions[user_id]["mana"] += 5
                    embed, view = await self.mining_interaction(interaction.user, False)
                    await interaction.response.edit_message(embed=embed, view=view)
                else:
                    user = interaction.message.embeds[0].author.name or "No idea"
                    await interaction.response.send_message(f"This menu belongs to {user}!", ephemeral=True)
            elif custom_id.startswith("blast"):
                if custom_id == f"blast-{user_id}":
                    self.active_sessions[user_id]["mana"] -= 20
                    embed, view = await self.mining_interaction(interaction.user, False)
                    await interaction.response.edit_message(embed=embed, view=view)
                else:
                    user = interaction.message.embeds[0].author.name or "No idea"
                    await interaction.response.send_message(f"This menu belongs to {user}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mine(bot))