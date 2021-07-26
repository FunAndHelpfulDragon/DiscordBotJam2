# import discord
from discord.ext import commands
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../Dna"))
import generation as g # noqa E402


class Dna(commands.Cog):
    def __init__(self, client):  # init this script
        self.client = client

    @commands.command()
    async def start(self, ctx):
        gen = g.Generation(ctx.author)  # change location
        if gen.GetInfo(ctx.author):
            await ctx.send("We have detected you already have a save, would you like to start again?")  # noqa

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            result = await self.client.wait_for('message', check=check)
            if result.content.lower() == "yes":
                if gen.DelGame(ctx.author):
                    await result.reply("Your save has been reset, use `!start` to get a new save")  # noqa
            elif result.content.lower() == "no":
                await ctx.send("Please use `COMMAND` to play")
        else:
            gen.Random(ctx.author, 7)
            await ctx.reply(embed=gen.LoadInv(ctx.author))
            await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))

    @commands.command(aliases=['Inv', 'inv', 'inventory'])
    async def Inventory(self, ctx):
        gen = g.Generation(ctx.author)  # change location
        await ctx.reply(embed=gen.LoadInv(ctx.author))
        await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))

    @commands.command()
    async def add(self, ctx, Colour=None, Place=None):
        if Colour is None:
            await ctx.reply("Please pick a colour")
        if Place is None or int(Place) < 0:
            await ctx.reply("Please pick a positive interager")
        gen = g.Generation(ctx.author)  # change location
        if Colour in gen.Inv(ctx.author, 'Inventory'):
            await ctx.reply("You do have this colour in your inventory!", mention_author=False)  # noqa
            gen.addInv(ctx.author, Colour, Place)
            await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))
        else:
            await ctx.reply("You do not have this colour in your inventory!")

    @commands.command()
    async def remove(self, ctx, Position=None):
        gen = g.Generation(ctx.author)  # change location
        if Position is None:
            await ctx.reply("Please enter a positive interager for the strand you want to take out")  # noqa
        gen.RmInv(ctx.author, Position)
        await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))


# setups the cog for use.
def setup(client):
    client.add_cog(Dna(client))
