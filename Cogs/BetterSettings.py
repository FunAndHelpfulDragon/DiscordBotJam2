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
        self.VView = False
        self.CChange = False

    async def view(self, ctx, edit):
        embed = discord.Embed(  # makes embed
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="Settings",
            value=f"Prefix: {await Lo.Info(ctx.guild.id, 'prefix')}\n" +  # noqa
                  f"Notifications: {await Lo.Info(ctx.guild.id, 'notifications')}\n"  # noq,  # better way than putting them all here?  # noqa
            )
        embed.set_footer(text=f"Tip: you can use {await Lo.Info(ctx.guild.id, 'prefix')}settings view or {await Lo.Info(ctx.guild.id, 'prefix')}settings change to view/change settings without having to say change/view after {await Lo.Info(ctx.guild.id, 'prefix')}settings\n")  # noqa
                              # f"Confused on what a setting does? use {await Lo.Info(ctx.guild.id, 'prefix')}help settings to view what each setting does.")  # noqa

        if edit:
            await ctx.edit(content="", embed=embed)
        else:
            await ctx.send(embed=embed)

    async def change(self, ctx):
        await ctx.message.delete()
        m1 = await ctx.send("What setting would you like to change?:")  # asks
        m2 = await ctx.send("Options: Prefix, Notifications (cancel = cancel)")  # noqa

        def check(m):  # checks
            return m.channel == ctx.channel

        msg = await self.client.wait_for('message', check=check)  # gets option # noqa
        savemsg = msg

        if msg.content == "cancel":
            await ctx.send("Caneled!")
            m1.message.delete()
            msg.message.delete()
            m2.message.delete()
        else:

            try:
                await msg.delete()

                result = await Lo.Info(ctx.guild.id, msg.content.lower())
                await m1.edit(content=f"Current {savemsg.content.lower()}: {result}")  # noqa says current
                await m2.edit(content="What would you like to change it to? (cancel to not change): ")  # noqa asks for update

                changesg = await self.client.wait_for('message', check=check)  # waits  # noqa
                if changesg.content == "cancel":
                    await ctx.send("Caneled!")
                    await m1.delete()
                    await changesg.delete()
                    await m2.delete()
                else:
                    await Lo.Save(ctx.guild.id, savemsg.content.lower(), changesg.content)  # updates  # noqa
                    await m1.delete()
                    await changesg.delete()
                    await m2.delete()
                    await ctx.send(f"{msg.content} has been changed to {changesg.content}")  # noqa
                    if msg.content.lower() == "prefix":
                        await ctx.guild.me.edit(nick=f"Run bot Run ({changesg.content})")  # noqa
            except Exception as e:  # change to something else
                await ctx.send(f"Recieved {e} whilst attempting to change setting")  # warning,  # noqa
                print(e)  # error in case

    @has_permissions(manage_guild=True)
    @commands.command(
        aliases=['settings', 'SETTINGS', 'setting', 'Setting', 'SETTING'],
        help="Shows/changes settings. Current settings:\n" +
        "Prefix,\n" +
        "Notifications (off = no notifications)\n",
        description="`option`: None, view, Change"
             )
    async def Settings(self, ctx, option="None"):
        if option.lower() == "view":
            await ctx.message.delete()
            await self.view(ctx, False)
        elif option.lower() == "change":
            await self.change(ctx)
        else:
            i = await ctx.send("What would you like to do (view or change):")

            def check(m):  # pretty pretty pretty sure this can be better.
                if m.content.lower() == "view":
                    self.VView = True
                elif m.content.lower() == "change":
                    self.CChange = True
                return m.channel == ctx.channel

            m3 = await self.client.wait_for('message', check=check)

        if self.VView:
            await m3.delete()
            await self.view(i, True)
        elif self.CChange:
            await m3.delete()
            await i.delete()
            await self.change(ctx)

        self.VView = False
        self.CChange = False


def setup(client):
    client.add_cog(Settings(client))
