from discord.ext import commands
from status import get_status
from db import session
from models import User

import discord
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

async def set_bot_presence():
    global bot
    await bot.change_presence(
        status=(discord.Status.online, discord.Status.dnd, discord.Status.idle)[get_status().value],
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Handeling EPITECH Intranet Events",
            state=("Online", "Offline", "Partially Online")[get_status().value],
        )
    )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await set_bot_presence()
    await tree.sync()

@tree.command(name="login", description="Register your token for a week")
async def login(interaction: discord.Interaction, token: str):
    # register_user(interaction.user, token)
    await interaction.response.send_message("Token saved !\nYou will receive events in DM.", ephemeral=True)

@tree.command(name="test")
async def test(interaction: discord.Interaction, user_id: int):
    print(f"Trying to find user {user_id} in DB")

    user = session.query(User).filter_by(id=user_id).first()

    await interaction.response.send_message(f"Found user {user}")

def run():
    bot.run(TOKEN)