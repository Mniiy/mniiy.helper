import discord, dotenv, os
dotenv.load_dotenv()

from discord.ext import commands

async def load(bot:commands.Bot, path:str):
    for file in os.listdir(path):
        if file.endswith(".py") and file!="__init__.py":
            await bot.load_extension(f"{path}.{file.removesuffix(".py")}")