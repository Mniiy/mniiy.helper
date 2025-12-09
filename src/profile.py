import discord

from discord.ext import commands

class profileCog(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        super().__init__()


    @commands.hybrid_group(
        name="profile",
        description="OwO (pq sempre o primeiro comando se chama \"hello\"?)"
    )
    async def profileGroup(self, ctx:commands.Context):
        await ctx.reply("hello, world")

    
async def setup(bot):
    await bot.add_cog(profileCog(bot))