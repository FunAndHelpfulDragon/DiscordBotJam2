import discord
from discord.ext import commands
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../Dna"))
import generation as g # noqa E402
import Running as r  # noqa E402
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import Load as L  # noqa
Lo = L.LoadFile()


class DNA(commands.Cog):
    def __init__(self, client):  # init this script
        self.client = client

    @commands.command(
        aliases=['Start'],
        help="Starts a game, Only 1 save file per user.",
        description="None",
        usage="None",
    )
    async def start(self, ctx):
        gen = g.Generation(ctx.author)  # change location
        if gen.GetInfo(ctx.author):  # checks if they already have game
            await ctx.send("We have detected you already have a save, would you like to start again? (Choice: yes, no)")  # noqa

            # see if they want to make a new game
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            result = await self.client.wait_for('message', check=check)
            if result.content.lower() == "yes":
                if gen.DelGame(ctx.author):
                    await result.reply("Your save has been reset, use `!start` to get a new save")  # noqa
            elif result.content.lower() == "no":
                await ctx.send(f"Please use `{await Lo.Info(ctx.guild.id, 'prefix')}inv`, `{await Lo.Info(ctx.guild.id, 'prefix')}run` to play")  # noqa
        else:  # makes a new game (remove/change else?)
            gen.Random(ctx.author, 7, True, True)
            await ctx.reply(embed=await gen.LoadInv(ctx.author))
            await ctx.reply(embed=await gen.LoadInv(ctx.author, 'DNA'))
            await self.Info(ctx)

    @commands.command(
        aliases=['Inv', 'inv', 'inventory'],
        help="Displays your inventory",
        description="None",
        usage="None",
    )
    async def Inventory(self, ctx):  # views their inventory
        gen = g.Generation(ctx.author)  # change location
        await ctx.reply(embed=await gen.LoadInv(ctx.author))
        await ctx.reply(embed=await gen.LoadInv(ctx.author, 'DNA'))
        await ctx.reply(f"use `{await Lo.Info(ctx.guild.id, 'prefix')}add` to move an strand from your inventory to your DNA, And use `{await Lo.Info(ctx.guild.id, 'prefix')}remove` to move a strand from your DNA to your inventory")  # noqa

    @commands.command(
        aliases=['Add'],
        help="Add a strand from your inventory to your DNA",
        description="`Colour`: option from your inventory, `Place`: Positive value",  # noqa
        usage="Colour (string), Place (int)"
        )
    # adds a strand to their dna
    async def add(self, ctx, Colour=None, Place=None):
        # checks
        if Colour is None:
            await ctx.reply("Please include a colour (name) from your inventory")  # noqa
        else:
            if Place is None or int(Place) < 0:
                await ctx.reply("Please include a positive interager of the space you want to put it in your DNA")  # noqa
        gen = g.Generation(ctx.author)  # change location
        # add
        result = await gen.Inv(ctx.author, 'Inventory')
        if Colour.lower() in result:
            # await ctx.reply("You do have this colour in your inventory!", mention_author=False)  # noqa
            await gen.addInv(ctx.author, Colour.lower(), Place)
            await ctx.reply(embed=await gen.LoadInv(ctx.author, 'DNA'))
            await ctx.reply(f"Use `{await Lo.Info(ctx.guild.id, 'prefix')}run` to see your results from your new DNA layout!")  # noqa
        else:
            await ctx.reply("You do not have this colour in your inventory!")

    @commands.command(
        aliases=['Remove', 'rm'],
        help="Removes a strand from your DNA and puts it in your inventory",
        description="`Position`: Value of position that strand is in",
        usage="Position (int)"
        )
    # removes strand from dna
    async def remove(self, ctx, Position=None):
        gen = g.Generation(ctx.author)  # change location
        if Position is None:
            await ctx.reply("Please enter a positive interager for the strand you want to take out")  # noqa
        else:
            await gen.RmInv(ctx.author, Position)
            await ctx.reply(embed=await gen.LoadInv(ctx.author, 'DNA'))
            await ctx.reply(f"Use `{await Lo.Info(ctx.guild.id, 'prefix')}run` to see your results from your new DNA layout!")  # noqa

    @commands.command(
        aliases=['clear_inv', 'clearInv', 'clearinventory', 'Clearinventory', 'Iclear'],  # noqa
        help="Empties your DNA into your inventory",  # noqa
        description="None",
        usage="None"
    )
    async def ClearInv(self, ctx):
        gen = g.Generation(ctx.author)  # change location
        for x in range(0, 10):
            await gen.RmInv(ctx.author, x)
        await ctx.send("Finished emptying DNA")

    @commands.command(
        aliases=['run'],
        help="Runs a simulation",
        description="None",
        usage="None"
    )
    async def Run(self, ctx):
        R = r.Running()
        embed = discord.Embed(
            name="Results",
            title="Results",
            description="Results of your recent running simulation (rounded to 5 decimal places)",  # noqa
            colour=discord.Colour.random()
        )
        X = 0
        Results = []
        random = False
        for rr in range(0, 10):
            if rr > 0:
                random = True
            Results.append(await R.Sim(ctx.author.id, random))

        await R.unlocked(ctx.author.id)
        for Result in Results:
            Result = str(Result)
            Result = Result.replace("[", "")
            Result = Result.replace("]", "")
            X += 1
            Extra = ""
            if X == 1:
                Extra = "(Yours)"
            embed.add_field(
                name=f"Runner {X} {Extra}",
                value=Result
            )
        embed.set_footer(
            text=f"{ctx.author}'s results"
        )
        msg = await ctx.send(embed=embed)
        Action, item = await R.Info(ctx.author, Results)
        if Action == "New Item":
            await msg.reply(f"You Recieved the '{item}' strand!")
        elif Action == "Loss":
            await msg.reply(f"You Lost the '{item}' strand :(")
        elif Action == "None":
            await msg.reply(f"You didn't come last, but you didn't come in the top half, so you got nothing :(")  # noqa
        elif Action == "Max":
            await msg.reply("You have gathered all the DNA alvalible. Well Done!")  # noqa
        else:
            await msg.reply("System broken, please contact an owner about this")  # noqa
        await ctx.reply(f"Use `{await Lo.Info(ctx.guild.id, 'prefix')}inventory` to see your inventory!")  # noqa

    @commands.command(
        aliases=['info'],
        help="Gives information about how to use the bot. PLEASE READ",
        description="None",
        usage="None",
    )
    async def Info(self, ctx):
        embed = discord.Embed(
            name="Welcome",
            description="WELCOME!",
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="Information",
            value="Welcome!, if you have started a new save or not, this embed is meant to teach you the basics."  # noqa
        )
        embed.add_field(
            name="Goal",
            value="Your goal, is to edit your DNA structure and try to get the best combination of DNA that there is. Using all 30 variations of strands (more coming soon). This is a running based simulation where each strand does different things to your bot. Use `!help colour` to get a list of colours."  # noqa
        )
        embed.add_field(
            name="Help",
            value=f"use `{await Lo.Info(ctx.guild.id, 'prefix')}help` to get information on commands."  # noqa
        )
        embed.add_field(
            name="Other Notes",
            value="- Your files save and load, so don't worry about losing data."  # noqa
        )
        embed.add_field(
            name="Basics",
            value=f"`{await Lo.Info(ctx.guild.id, 'prefix')}inv` is your inventory where you have all your strands.\n" +  # noqa
            f"To add strands to your DNA use `{await Lo.Info(ctx.guild.id, 'prefix')}add` along with the colour of the strand and the position. Do note, that you can only put 1 strand in each position.\n" +  # noqa
            f"To remove strands from your DNA use `{await Lo.Info(ctx.guild.id, 'prefix')}remove` along with the place the strand is in the DNA.\n" +  # noqa
            f"To test out your DNA against other bots (and possibly get more) use `{await Lo.Info(ctx.guild.id, 'prefix')}run`.\n" +  # noqa
            f" Your challenge is to get the highest score out of all the bots.\n" +  # noqa
            f"New strands are Recieved from doing `{await Lo.Info(ctx.guild.id, 'prefix')}run` But be carefuly as you can lose a strand.\n" +  # noqa
            f"Each strand has different abilities, some are good and some are bad.",  # noqa
            inline=False
        )
        embed.set_footer(
            text=f"{ctx.author}'s game"
        )
        await ctx.send(embed=embed)

    @start.error
    async def start_fail_Error(self, ctx, error):
        await ctx.send("There was a failure whilst starting a new game, please try again\n If it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:start->{error}")

    @Inventory.error
    async def Inventory_fail_Error(self, ctx, error):
        await ctx.send("There was an error whilst trying to show your inventory, please try again\n If it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:Inventory->{error}")

    @add.error
    async def add_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst adding a strand to your DNA,  please try again\n If it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:add->{error}")

    @remove.error
    async def remove_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst removing a strand from your DNA,  please try again\n If it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:remove->{error}")

    @Run.error
    async def run_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst your runners were trying to run, please try again.\nIf it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:run->{error}")

    @Info.error
    async def info_fail_error(self, ctx, error):
        await ctx.send("There was an error whilst trying to show you some information, please try again.\nIf it happens again, please alert one of the owners")  # noqa
        print(f"{ctx.author}:Info->{error}")


# setups the cog for use.
def setup(client):
    client.add_cog(DNA(client))
