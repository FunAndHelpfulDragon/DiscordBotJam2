from discord.ext import commands

prefixs = "!", "/",  # "BOT PING HERE"

client = commands.Bot(
    command_prefix=prefixs,
    description="Discord Bot Jam 2 Bot"
)


@client.event
async def on_ready():
    print("Bot is ready")


def GetKey():
    file = open("Key.txt", "r")  # reads the key
    key = file.read()
    file.close()
    return key


@client.command(
    description="Loads a cog (limited to developers)"
)
async def Load(ctx, extension):
    if ctx.author.id == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
        client.load_extension(f'Cogs.{extension}')  # loads a cog
        print(f'Cog:{extension} Loaded')


@client.command(
    description="Unloads a cog (limited to developers)"
)
async def UnLoad(ctx, extension):
    if ctx.author.id  == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
        client.unload_extension(f'Cogs.{extension}')  # unloads a cog
        print(f'Cog:{extension} Unloaded')


# error checking
# XXX: make it so that we know the cog that failed to load.
@Load.error
async def Load_Fail_Error(ctx, error):
    await ctx.send("There was an error whilst loading the cog.")
    print(error)


@UnLoad.error
async def UnLoad_Fail_Error(ctx, error):
    await ctx.send("There was an error whilst unloading the cog.")
    print(error)


client.run(GetKey())  # runs bot
