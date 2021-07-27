# import discord
from discord.ext import commands
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../Dna"))
import generation as g # noqa E402


class Dna(commands.Cog):
    def __init__(self, client):  # init this script
        self.client = client

    @commands.command(
        aliases=['Start'],
        help="Starts a game, Only 1 save file per user."
    )
    async def start(self, ctx):
        gen = g.Generation(ctx.author)  # change location
        if gen.GetInfo(ctx.author):  # checks if they already have game
            await ctx.send("We have detected you already have a save, would you like to start again?")  # noqa

            # see if they want to make a new game
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            result = await self.client.wait_for('message', check=check)
            if result.content.lower() == "yes":
                if gen.DelGame(ctx.author):
                    await result.reply("Your save has been reset, use `!start` to get a new save")  # noqa
            elif result.content.lower() == "no":
                await ctx.send("Please use `COMMAND` to play")
        else:  # makes a new game (remove/change else?)
            gen.Random(ctx.author, 7)
            await ctx.reply(embed=gen.LoadInv(ctx.author))
            await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))

    @commands.command(
        aliases=['Inv', 'inv', 'inventory'],
        help="Displays your inventory"
    )
    async def Inventory(self, ctx):  # views their inventory
        gen = g.Generation(ctx.author)  # change location
        await ctx.reply(embed=gen.LoadInv(ctx.author))
        await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))

    @commands.command(
        aliases=['Add'],
        help="Add a strand from your inventory to your dna"
        )
    # adds a strand to their dna
    async def add(self, ctx, Colour=None, Place=None):
        # checks
        if Colour is None:
            await ctx.reply("Please pick a colour")
        if Place is None or int(Place) < 0:
            await ctx.reply("Please pick a positive interager")
        gen = g.Generation(ctx.author)  # change location
        # add
        if Colour in gen.Inv(ctx.author, 'Inventory'):
            await ctx.reply("You do have this colour in your inventory!", mention_author=False)  # noqa
            gen.addInv(ctx.author, Colour, Place)
            await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))
        else:
            await ctx.reply("You do not have this colour in your inventory!")

    @commands.command(
        aliases=['Remove', 'rm'],
        help="Removes a strand from your dna and puts it in your inventory"
        )
    # removes strand from dna
    async def remove(self, ctx, Position=None):
        gen = g.Generation(ctx.author)  # change location
        if Position is None:
            await ctx.reply("Please enter a positive interager for the strand you want to take out")  # noqa
        else:
            gen.RmInv(ctx.author, Position)
            await ctx.reply(embed=gen.LoadInv(ctx.author, 'Strands'))

    @start.error
    async def start_fail_Error(self, ctx, error):
        await ctx.send("There was a failure whilst starting a new game, please try again\n If it happens again, please alert on of the owners")  # noqa
        print(f"{ctx.author}:start->{error}")

    @Inventory.error
    async def Inventory_fail_Error(self, ctx, error):
        await ctx.send("There was an error whilst trying to show your inventory, please try again\n If it happens again, please alert on of the owners")  # noqa
        print(f"{ctx.author}:Inventory->{error}")

    @add.error
    async def add_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst adding a strand to your dna,  please try again\n If it happens again, please alert on of the owners")  # noqa
        print(f"{ctx.author}:add->{error}")

    @remove.error
    async def remove_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst removing a strand from your dna,  please try again\n If it happens again, please alert on of the owners")  # noqa
        print(f"{ctx.author}:remove->{error}")


# setups the cog for use.
def setup(client):
    client.add_cog(Dna(client))
