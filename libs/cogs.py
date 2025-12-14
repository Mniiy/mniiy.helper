import os

async def loadFile(bot, path:str):
    if path.endswith(".py"):
            await bot.load_extension(f"{path}.{file}")

async def loadFolder(bot, path:str):
    for file in os.listdir(path):
        if file.endswith(".py"):
            print(file)
            await bot.load_extension(f"{path}.{file.removesuffix(".py")}")