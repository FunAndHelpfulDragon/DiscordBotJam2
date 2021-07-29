import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import Load  # noqa E402
Lo = Load.LoadFile()


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.view = False
        self.change = False

    @has_permissions(manage_guild=True)
    @commands.command(
        aliases=['settings', 'SETTINGS'],
        help="Shows/changes settings. Current settings:\n" +
        "Prefix,\n" +
        "Notifications,\n" +
        "NC (Notifications Channel)"
             )
    async def Settings(self, ctx, option="None"):
        # option is for if they just want to go straight there
        # XXX: add optional value for even quicker use (e.g. change prefix:
        # {prefix}settings change prefix)???

        async def view():  # view settings
            embed = discord.Embed(
                    colour=discord.Colour.red())  # setting to change?
            embed.add_field(  # automatic?
                    name="Settings",
                    value=f"Prefix: {Lo.Info(ctx.guild.id, 'prefix')}\n" +
                          f"Notifications: {Lo.Info(ctx.guild.id, 'notifications')}\n" +  # noqa
                          f"Notifications Channel: {Lo.Info(ctx.guild.id, 'nc')}",  # better way than putting them all here?  # noqa
                    )
            embed.set_footer(text="Tip: you can use !settings view or !settings change to view/change settings without having to say change/view after !settings")  # noqa
            await ctx.send(embed=embed)

        async def change():
            await ctx.send("What setting would you like to change?:")  # asks
            await ctx.send("Options: Prefix, Notifications, NC (Notifications channel)")  # noqa

            def ccheck(m):  # checks
                return m.channel == ctx.channel

            msg = await self.client.wait_for('message', check=ccheck)  # gets option # noqa
            try:
                result = Lo.Info(ctx.guild.id, msg.content.lower())
                await ctx.send(f"Current {msg.content.lower()}: {result}")  # noqa says current
                await ctx.send("What would you like to change it to? (cancel to not change): ")  # noqa asks for update

                changesg = await self.client.wait_for('message', check=ccheck)  # waits  # noqa
                if changesg.content == "cancel":
                    await ctx.send("Caneled!")
                else:
                    Lo.Save(ctx.guild.id, msg.content.lower(), changesg.content)  # updates  # noqa
                    await ctx.send(f"{msg.content} has been changed to {changesg.content}")  # noqa
            except Exception as e:  # change to something else
                await ctx.send(f"Recieved {e} whilst attempting to change setting")  # warning,  # noqa
                print(e)  # error in case

        if option.lower() == "view":  # shortcut
            await view()
        elif option.lower() == "change":
            await change()
        else:
            await ctx.send("What would you like to do (view or change):")

            def check(m):  # pretty pretty pretty sure this can be better.
                if m.content.lower() == "view":
                    self.view = True
                elif m.content.lower() == "change":
                    self.change = True
                return m.channel == ctx.channel

            await self.client.wait_for('message', check=check)

        if self.view:
            await view()
        elif self.change:
            await change()

        self.view = False
        self.change = False

    # @commands.command()


def setup(client):
    client.add_cog(Settings(client))
