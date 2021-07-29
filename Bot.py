from discord.ext import commands
from dpyConsole import Console
import os
import Load as L
Lo = L.LoadFile()


async def get_prefix(client, message):
    try:  # try except makes it work in dm's
        result = Lo.Info(message.guild.id, "prefix")
        print(result)
        return result
    except Exception:  # change exception?
        return '!'


client = commands.Bot(
    command_prefix=get_prefix,
    description="Discord Bot Jam 2 Bot"
)
my_console = Console(client)

client.remove_command('help')


# remove settings for server on leave?
# @client.event
# async def on_guild_remove(guild):
#     if os.path.exists(f"Files/{guild}"):
#         os.remove(f"Files/{guild}")

@my_console.command()
async def Notify(message):
    print("Sending message to discord")
    print(os.walk("Files"))
    print("2")
    for r, d, file in os.walk("Files/"):
        for file in file:
            print(file)
            if file.endswith(".server"):
                print(f"{file} ends with '.server'")
                if Lo.Info(file[:-7], 'notifications').lower() == "true":
                    Channel = int(Lo.Info(file[:-7], 'nc'))
                    channel = client.get_channel(Channel)
                    await channel.send(message)


@client.event
async def on_ready():
    print("Bot is ready")


def GetKey():
    with open("Key.txt", "r") as Key:  # reads the key
        return Key.read()


@client.command(
    description="Loads a cog (limited to developers)",
    aliases=['Load', 'load'],
    hidden=True
)
@commands.is_owner()
async def _Load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')  # loads a cog
    print(f'Cog: {extension} Loaded')


@client.command(
    description="Unloads a cog (limited to developers)",
    aliases=['UnLoad', 'unload', 'Unload'],
    hidden=True
)
@commands.is_owner()
async def _UnLoad(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')  # unloads a cog
    print(f'Cog: {extension} Unloaded')


@client.command(
    description="Reload a cog (limited to developers)",
    aliases=['Reload', 'reload'],
    hidden=True
)
@commands.is_owner()
async def _Reload(ctx, extension=None):
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
    aliases=['ListCogs', 'List'],
    hidden=True
)
@commands.is_owner()
async def _ListCogs(ctx):  # no need to check as it can't do anything.
    await ctx.send("Cogs in folder: ")
    for filename in os.listdir("./Cogs"):
        if filename != "__pycache__":  # add no cogs here
            await ctx.send(filename[:-3])


# error checking
# XXX: make it so that we know the cog that failed to load.
@_Load.error
async def Load_Fail_Error(ctx, error):
    print(error)


@_UnLoad.error
async def UnLoad_Fail_Error(ctx, error):
    print(error)


@_Reload.error
async def Reload_Fail_Error(ctx, error):
    print(error)


@_ListCogs.error
async def ListCogs_Fail_Error(ctx, error):
    print(error)


if __name__ == '__main__':
    for Cog in os.listdir("./Cogs"):
        if Cog != "__pycache__" and Cog != ".DS_Store":  # add no cogs here
            client.load_extension(f'Cogs.{Cog[:-3]}')  # removes ".py" extension + loads cog  # noqa

    my_console.start()
    client.run(GetKey())  # runs bot
