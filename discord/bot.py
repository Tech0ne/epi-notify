from discord.ext import commands
from status import get_status
from db import session
from models import User

import discord
import sys
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

async def _send_dm(user_id: int, message: str):
    global bot

    user = bot.get_user(user_id)
    print(user, file=sys.stderr)
    await user.send(message)

def send_dm(user_id: int, message: str):
    global bot
    bot.loop.create_task(_send_dm(user_id, message))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await set_bot_presence()
    await tree.sync()

@tree.command(name="login", description="Register your token for a week")
async def login(ctx: discord.Interaction, token: str):
    # register_user(ctx.user, token)
    await ctx.response.send_message("Token saved !\nYou will receive events in DM.", ephemeral=True)

def run():
    bot.run(TOKEN)