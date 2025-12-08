import discord, dotenv, os, sys
from database.UserDatabase import UserDatabase
from discord.ext import commands

from libs import cogs
from libs.usr import User
dotenv.load_dotenv()


class ClassBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=[".", ". "])
    
    async def on_ready(self):
        await cogs.load(BOT, "src")
    
    def Run(self):
        tkn=os.getenv("tkn")
        self.run(tkn)


BOT= ClassBot()

if __name__== "__main__":
    BOT.Run()