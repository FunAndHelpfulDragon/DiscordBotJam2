from discord.ext import commands
import os
import Load as L
Lo = L.LoadFile()

prefixs = "!", "/",  # "BOT PING HERE"


def get_prefix(client, message):
    result = Lo.Info(message.guild.id, "prefix")
    print(result)
    return result


client = commands.Bot(
    command_prefix=get_prefix,
    description="Discord Bot Jam 2 Bot"
)

client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is ready")


def GetKey():
    file = open("Key.txt", "r")  # reads the key
    key = file.read()
    file.close()
    return key


@client.command(
    description="Loads a cog (limited to developers)",
    aliases=['Load', 'load']
)
async def _Load(ctx, extension):
    # this if statement VV can we do something about it?
    if ctx.author.id == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
        client.load_extension(f'Cogs.{extension}')  # loads a cog
        print(f'Cog: {extension} Loaded')


@client.command(
    description="Unloads a cog (limited to developers)",
    aliases=['UnLoad', 'unload', 'Unload']
)
async def _UnLoad(ctx, extension):
    if ctx.author.id  == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
        client.unload_extension(f'Cogs.{extension}')  # unloads a cog
        print(f'Cog: {extension} Unloaded')


@client.command(
    description="Reload a cog (limited to developers)",
    aliases=['Reload', 'reload']
)
async def _Reload(ctx, extension=None):
    if ctx.author.id  == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
        if extension is not None:
            client.unload_extension(f'Cogs.{extension}')
            client.load_extension(f'Cogs.{extension}')
            await ctx.send(f"Reloaded {extension}")
        else:
            for Cog in os.listdir("./Cogs"):
                if Cog != "__pycache__":  # add no cogs here
                    client.unload_extension(f'Cogs.{Cog[:-3]}')
                    client.load_extension(f'Cogs.{Cog[:-3]}')
            await ctx.send("Reloaded cogs")


@client.command(
    description="List all cogs (not limited)",
    aliases=['ListCogs', 'List']
)
async def _ListCogs(ctx):  # no need to check as it can't do anything.
    await ctx.send("Cogs in folder: ")
    for filename in os.listdir("./Cogs"):
        if filename != "__pycache__":  # add no cogs here
            await ctx.send(filename[:-3])


# error checking
# XXX: make it so that we know the cog that failed to load.
@_Load.error
async def Load_Fail_Error(ctx, error):
    await ctx.send("There was an error whilst loading the cog.")
    print(error)


@_UnLoad.error
async def UnLoad_Fail_Error(ctx, error):
    await ctx.send("There was an error whilst unloading the cog.")
    print(error)


@_Reload.error
async def Reload_Fail_Error(ctx, error):
    await ctx.send("There was an error whilst trying to reload the cog.")
    print(error)


@_ListCogs.error
async def ListCogs_Fail_Error(ctx, error):
    await ctx.send("There was an errpr whilst listing the cogs")
    print(error)


for Cog in os.listdir("./Cogs"):
    if Cog != "__pycache__":  # add no cogs here
        client.load_extension(f'Cogs.{Cog[:-3]}')  # removes ".py" extension + loads cog  # noqa


client.run(GetKey())  # runs bot
