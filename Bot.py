from discord.ext import commands
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

client.remove_command('help')


# remove settings for server on leave?
# @client.event
# async def on_guild_remove(guild):
#     if os.path.exists(f"Files/{guild}"):
#         os.remove(f"Files/{guild}")


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
        if Cog != "__pycache__":  # add no cogs here
            client.load_extension(f'Cogs.{Cog[:-3]}')  # removes ".py" extension + loads cog  # noqa

    client.run(GetKey())  # runs bot
