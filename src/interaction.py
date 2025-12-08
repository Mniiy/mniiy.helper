import discord

from discord.ext import commands

class interaction(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        super().__init__()


    @commands.command(
        name="hello",
        description="OwO (pq sempre o primeiro comando se chama \"hello\"?)"
    )
    async def helloCommand(self, ctx:commands.Context):
        await ctx.reply("hello, world")

    
async def setup(bot):
    await bot.add_cog(interaction(bot))