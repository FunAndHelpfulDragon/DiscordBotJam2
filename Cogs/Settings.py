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

    @has_permissions(administrator=True)
    @commands.command(aliases=['settings', 'SETTINGS'])
    async def Settings(self, ctx, option="None"):
        # option is for if they just want to go straight there

        def view():  # view settings
            embed = discord.Embed(
                    colour=discord.Colour.red())  # setting to change?
            embed.add_field(
                    name="Settings",
                    value=f"Prefix: {Lo.Info(ctx.guild.id, 'Prefix')}",  # better way than putting them all here?  # noqa
                    )
            return embed

        async def change():
            await ctx.send("What setting would you like to change?:")  # asks
            await ctx.send("Options: Prefix")

            def ccheck(m):  # checks
                return m.channel == ctx.channel

            msg = await self.client.wait_for('message', check=ccheck)  # gets option # noqa
            try:
                result = Lo.Info(ctx.guild.id, msg.content.lower())
                await ctx.send(f"Current {msg.content.lower()}: {result}")  # noqa says current
                await ctx.send("What would you like to change it to? (cancel to not change): ")  # noqa asks for update

                changesg = await self.client.wait_for('message', check=ccheck)  # waits  # noqa
                Lo.Save(ctx.guild.id, msg.content.lower(), changesg.content)  # updates  # noqa
                await ctx.send(f"{msg.content} has been changed to {changesg.content}")  # noqa
            except Exception as e:  # change to something else
                await ctx.send(f"Recieved {e} whilst attempting to change setting")  # warning,  # noqa
                print(e)  # error in case

        if option.lower() == "view":  # shortcut
            await ctx.send(embed=view())
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
            await ctx.send(embed=view())
        elif self.change:
            await change()

        self.view = False
        self.change = False

    # @commands.command()


def setup(client):
    client.add_cog(Settings(client))
