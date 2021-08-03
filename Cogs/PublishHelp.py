import discord
from discord.ext import commands
import CleanHelp as Clean
import asyncio


class PublishHelp(commands.Cog, description="Help about Help (also about and credit)"):  # noqa
    def __init__(self, client, pages, colour):
        print("Publish Help setup")
        self.client = client
        self.CH = Clean.CleanHelp(self.client, colour)
        self.pages = pages
        self.page = 0

    @commands.command(
        aliases=['Help', 'HELP'],
        help="Help? Come need help?",
        description="None",
        usage="None"
    )
    async def help(self, ctx, Page=0):
        self.Page = Page  # get page
        self.pages = self.CH.makePages([])  # get pages
        msg = await ctx.send(embed=self.pages[self.Page])  # send page of pages
        if self.Page > 0:
            await msg.add_reaction("⬅️")  # add reactions (if conditions meet)
        if self.Page < 3:
            await msg.add_reaction("➡️")

        await msg.add_reaction("❌")

        def check(reaction, user):  # check for reactions
            if not user.bot and reaction.message == msg:
                if str(reaction.emoji) == "⬅️":
                    self.Page -= 1
                elif str(reaction.emoji) == "➡️":
                    self.Page += 1
                elif str(reaction.emoji) == "❌":
                    self.Page = -1
                return True

        while self.Page != -1:  # while not close
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=600, check=check)  # 600 = 10mins # noqa
                await msg.remove_reaction(reaction, user)
                if self.Page != -1:
                    try:
                        await msg.edit(embed=self.pages[self.Page])  # edits with new  # noqa
                    except IndexError:
                        if self.Page > 3:
                            self.Page = 3
                        elif self.Page < 0:
                            self.Page = 0
                        else:
                            await ctx.send("how? how did you break this?")
                        await msg.edit(embed=self.pages[self.Page])
                    if self.Page > 0:  # more reactions
                        await msg.add_reaction("⬅️")
                    else:
                        await msg.clear_reaction("⬅️")
                    if self.Page < 3:
                        await msg.add_reaction("➡️")
                    else:
                        await msg.clear_reaction("➡️")
                    await msg.add_reaction("❌")
            except asyncio.TimeoutError:  # timeout
                await msg.delete()
        else:  # delete but keep
            await msg.remove_reaction("⬅️", msg.author)
            await msg.remove_reaction("➡️", msg.author)
            await msg.remove_reaction("❌", msg.author)

    @commands.command(
        aliases=['ColorHelp', 'colourhelp', 'colorhelp', 'Ch', 'ch', 'CH'],
        help="Shows colours, and what category they come in",
        description="None",
        usage="None"
    )
    async def ColourHelp(self, ctx):
        embed = discord.Embed(
            title="Colours",
            description="A list of colours and what category they come under, for a good bot you need at least 1 strand (colour) in 'Speed', 'Energy', 'Nodes', 'Time'",  # noqa
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="Speed",
            value="red, light blue, dark green, amber, canary, gold",
            inline=False
        )
        embed.add_field(
            name="Energy",
            value="orange, light green, green, blue, dark blue, bronze, coral, desert",  # noqa
            inline=False
        )
        embed.add_field(
            name="Nodes",
            value="yellow, purple, pink, charcol, flame, frostbite",
            inline=False
        )
        embed.add_field(
            name="Time",
            value="white, grey, cyan, carrot orange, lemon, jungle green",
            inline=False
        )
        embed.add_field(
            name="Nothing",
            value="black, cadet, iceberg, mango",
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=['About', 'ABOUT'],
        help="Information about the bot",
        description="None",
        usage="None"
    )
    async def about(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.random(),
            # title="Credit"
        )
        embed.add_field(
            name="About",
            value="This is a bot made for the discord bot jam 2 (https://itch.io/dbj2) designed by: dragmine149#5048 and Guy_372#4809.\n" +  # noqa
                  "NOTES:\n" +
                  "- The theme is hard, so this bot took a while to make.\n" +
                  "- Getting the results is done by maths, Not by actually running a simulation. This is easier and quicker.\n" +  # noqa
                  "  Even though it is done like this, hopefully you can see how it still fits the theme."  # noqa
        )
        embed.set_footer(
            text="Want to invite this bot? Do so here!: https://discord.com/api/oauth2/authorize?client_id=868506788666966056&permissions=2214718464&scope=bot"  # noqa
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=['credit', 'credits'],
        help="Shows who has helped on the bot",
        description="None",
        usage="None"
    )
    async def Credit(self, ctx):
        embed = discord.Embed(
            name="Credits",
            description="People who have worked on the bot",
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="dragmine149#5048",
            value="Owner, Programming.",
            inline=True
        )
        embed.add_field(
            name="Guy_732#4809",
            value="Programming. (tidied up some of the code for me, thanks. unfortunately that was all that was possibly in the time limit)",  # noqa
            inline=True
        )
        embed.add_field(
            name="RebeccaBanner#4912",
            value="Tester, helped with some other things as well."
        )
        embed.set_footer(
            text="Please do not attempt to direct message one of these to get them to do so, If you try to it might result in a block from them."  # noqa
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PublishHelp(client, [], discord.Colour.random()))
