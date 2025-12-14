import discord, os
import libs.cogs as cogs


from discord.ext import commands
# internet podre-


class Gyawn(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=[".", ". "])

    async def on_ready(self):
        await cogs.loadFolder(self, "cmds")

    