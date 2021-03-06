import discord
from discord.ext import commands

with open("Test.txt", 'r') as Test:
    result = int(Test.read())
    if result == 0:
        ConsoleCheck = input("Check for console input? (y = yes, n = no):")
        if ConsoleCheck.lower() == "y":
            from dpyConsole import Console
    else:
        ConsoleCheck = "n"

import os  # noqa
import Load as L  # noqa
Lo = L.LoadFile()


async def get_prefix(client, message):
    try:  # try except makes it work in dm's
        result = await Lo.Info(message.guild.id, "prefix")
        print(result)
        return result
    except Exception:  # change exception?
        return '!'


client = commands.Bot(
    command_prefix=get_prefix,
    description="Discord Bot Jam 2 Bot"
)
if ConsoleCheck.lower() == "y":
    my_console = Console(client)

client.remove_command('help')


# remove settings for server on leave?
# @client.event
# async def on_guild_remove(guild):
#     if os.path.exists(f"Files/{guild}"):
#         os.remove(f"Files/{guild}")

if ConsoleCheck.lower() == "y":
    @my_console.command()
    async def Notify(message):
        print("Sending message to discord")
        for r, d, file in os.walk("Files/"):
            for file in file:
                print(file)
                if file.endswith(".server"):
                    print(f"{file} ends with '.server'")
                    if await Lo.Info(file[:-7], 'Notifications').lower() != "off":  # noqa
                        Channel = int(await Lo.Info(file[:-7], 'Notifications'))  # noqa
                        channel = client.get_channel(Channel)
                        await channel.send(message)
                        break


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                name="Welcome",
                title="Welcome",
                description="Thank you for inviting me, here is some information."  # noqa
            )
            embed.add_field(
                name="Settings",
                value="The prefix for this server is '!' by deafult, although can be changed."  # noqa
            )
            embed.add_field(
                name="Commands",
                value="All of my commands are in '!help'"
            )
            await channel.send(embed=embed)
    await guild.me.edit(nick="Run bot Run (!)")


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
            if Cog != "__pycache__" or Cog != ".DS_Store":  # add no cogs here
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
        if filename != "__pycache__" or filename == ".DS_Store":  # add no cogs
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
    # client.load_extension('Cogs.PublishHelp')

    if ConsoleCheck.lower() == "y":
        my_console.start()
    client.run(GetKey())  # runs bot
