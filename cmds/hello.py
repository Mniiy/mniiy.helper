from libs.Gyawn import Gyawn
from discord.ext import commands

class helloCog(commands.Cog):
    def __init__(self, bot:Gyawn):
        pass

    @commands.hybrid_command(
        name="hello",
        description="Says hello"
    )
    async def helloCommand(self, ctx:commands.Context):
        await ctx.send(f"hello, {ctx.author.mention}!")





async def setup(bot:Gyawn):
    await bot.add_cog(helloCog(bot))