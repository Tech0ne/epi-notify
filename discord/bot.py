from discord.ext import commands
from status import get_status
from db import session
from models import User, Hook
from urllib.parse import urljoin

from hashlib import md5

import discord
import jwt
import sys
import os

TOKENS_CHANNEL = os.getenv("DISCORD_TOKENS_CHANNEL")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
NTFY_URL = os.getenv("NTFY_BASE_URL")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

def register_token(user = None, token = None, author = None):
    if token is None:
        return
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        print(f"[+] Got error {e} while decoding JWT", file=sys.stderr)
        return
    login = payload.get("login")

    if user is None:
        if author is not None:
            user = session.query(User).filter_by(discord_id=author).first()
        elif login is not None:
            user = session.query(User).filter_by(email=login).first()

    if user is None:
        return

    if login is not None:
        user.email = login
    if author is not None:
        user.discord_id = author
    user.token = token
    session.commit()

def register_ntfy(user):
    if user is None:
        return "[ERROR]"
    url = md5(os.urandom(16)).hexdigest()
    while session.query(User).filter_by(ntfy_url=url).first() is not None:
        url = md5(os.urandom(16)).hexdigest()
    return url

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

def create_user_from_discord(discord_id: int):
    session.commit()
    user = session.query(User).filter_by(discord_id=discord_id).first()
    if user is None:
        user = User(
            discord_id=discord_id
        )
        session.add(user)
        session.commit()
    return user

@bot.event
async def on_message(message):
    if str(message.channel.id) != str(TOKENS_CHANNEL):
        return
    token = message.content
    register_token(None, token, None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await set_bot_presence()
    await tree.sync()

@tree.command(name="ntfy", description="Regenerate your Ntfy URL")
async def ntfy(ctx: discord.Interaction):
    user = create_user_from_discord(ctx.user.id)
    if user.email is None:
        await ctx.response.send_message(f"Could not create NTFY url without token !\nPlease login first using the `/login` command !")
        return
    url = register_ntfy(user)
    user.ntfy_url = url
    session.commit()
    await ctx.response.send_message(f"Here is your new ntfy url: `{urljoin(NTFY_URL, url)}`")

@tree.command(name="login", description="Register your token for a week")
async def login(ctx: discord.Interaction, token: str = None):
    if token is None:
        await ctx.response.send_message("Please paste your intranet token !\nSee <#1305141459267092554> for detailed instructions")
        return
    user = create_user_from_discord(ctx.user.id)
    register_token(user, token, ctx.user.id)
    await ctx.response.send_message("Token saved !\nYou will receive events in DM.", ephemeral=True)

def run():
    bot.run(TOKEN)