import discord

from discord.ext import commands
# internet podre-


class Gyawn(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.intents.all(), command_prefix=[".", ". "])
    

    async def on_ready(self):
        print("ready")

    