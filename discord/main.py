import discord
from discord.ext import commands
from enum import Enum
import os

class Status(Enum):
    OK = 0
    KO = 1
    NA = 2

STATUS = Status.OK

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def set_bot_presence():
    await bot.change_presence(
        status=(discord.Status.online, discord.Status.dnd, discord.Status.idle)[STATUS.value],
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Handeling EPITECH Intranet Events",
            state=("Online and running", "Failed to access ressources", "Online but not working properly")[STATUS.value],
        )
    )

@bot.event
async def on_ready():
    await set_bot_presence()
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.command()
async def login(ctx, api_key: str):
    if ctx.guild is None:
        await ctx.send("Login token saved. Thank you !\nEvents will be sent to you here.")
        print(f"Received API key from {ctx.author}: {api_key}")
    else:
        await ctx.message.delete()
        await ctx.author.send("Please use this command here in order to register your account.")

bot.run(TOKEN)