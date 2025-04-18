"""
# to generate "requirements.txt", do:
# pipreqs /path/to/project
"""

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="你"))
    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] Bot is ready')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return 0

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def reload(ctx, cog: str):
    
    # See if "Admin.txt" exists, if not, create one.
    try:
        f = open('./data/Admin.txt', 'r', encoding='utf-8')
        tmp = f.read()
        ADMIN_ID_LIST = tmp.split('\n')
        f.close()
    except FileNotFoundError:
        await ctx.send("建立機器人維護者資料...")
        with open('./data/Admin.txt', 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
        await ctx.send("建立完成")
    
    if str(ctx.message.author.id) not in ADMIN_ID_LIST:
        await ctx.send("錯誤，不是機器人維護者")
        return 0
    
    await bot.reload_extension(f"cogs.{cog.lower()}")
    await ctx.send("已刷新")
    

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())