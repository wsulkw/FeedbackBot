from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
from discord.interactions import Interaction

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=">", intents=intents)


class FeedbackBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1164362273175896107))
        self.synced = True
        print(f"Logged in as {self.user}")


bot = FeedbackBot()
tree = app_commands.CommandTree(bot)


class FeedbackModal(discord.ui.Modal, title="Feedback"):
    subject = discord.ui.TextInput(label="Subject", placeholder="Please specify the subject of your feedback.", required=True, style=discord.TextStyle.short)
    content = discord.ui.TextInput(label="Description", placeholder="Please enter your detailed feedback here.", required=True, style=discord.TextStyle.long)


    async def on_submit(self, interaction: Interaction):
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"logs/{interaction.user.name} {timestamp_str}", "w") as f:
            f.write(f"Subject: {self.subject}")
            f.write(f"\nDescription: {self.content}")

        await interaction.guild.owner.send(f"New feedback has been logged by {interaction.user}")

        await interaction.response.send_message(f"{interaction.user.mention} Thank you for submitting your feedback!", ephemeral=True)

        
@tree.command(name="feedback", description="Send feedback to the admins.", guild=discord.Object(id=1164362273175896107))
@app_commands.checks.cooldown(1, 3600.0*24)
async def self(interaction: discord.Interaction):
    await interaction.response.send_modal(FeedbackModal())



bot.run("")
