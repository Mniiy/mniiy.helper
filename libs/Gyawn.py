import discord
from discord.ext import Commands


# internet podre-


class Gyawn(Commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.intents.all())

    