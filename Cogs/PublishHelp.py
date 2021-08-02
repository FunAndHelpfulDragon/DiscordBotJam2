import discord
from discord.ext import commands
import CleanHelp as Clean
import asyncio


class PublishHelp(commands.Cog):
    def __init__(self, client, pages, colour):
        print("Publish Help setup")
        self.client = client
        self.CH = Clean.CleanHelp(self.client, colour)
        self.pages = pages
        self.page = 0

    @commands.command()
    async def help(self, ctx, Page=0):
        self.Page = Page
        self.pages = self.CH.makePages([])
        msg = await ctx.send(embed=self.pages[self.Page])
        if self.Page > 0:
            await msg.add_reaction("⬅️")
        if self.Page < 3:
            await msg.add_reaction("➡️")
        await msg.add_reaction("❌")

        def check(reaction, user):
            if user == ctx.author:
                if str(reaction.emoji) == "⬅️":
                    self.Page -= 1
                elif str(reaction.emoji) == "➡️":
                    self.Page += 1
                elif str(reaction.emoji) == "❌":
                    self.Page = -1
            return True

        while self.Page != -1:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=10000000000000000, check=check)  # noqa
                await msg.remove_reaction(reaction, user)
                if self.Page != -1:
                    await msg.edit(embed=self.pages[self.Page])
                    if self.Page > 0:
                        await msg.add_reaction("⬅️")
                    else:
                        await msg.clear_reaction("⬅️")
                    if self.Page < 3:
                        await msg.add_reaction("➡️")
                    else:
                        await msg.clear_reaction("➡️")
            except asyncio.TimeoutError:
                await msg.delete()
        else:
            await msg.remove_reaction("⬅️", msg.author)
            await msg.remove_reaction("➡️", msg.author)
            await msg.remove_reaction("❌", msg.author)

    @commands.command()
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
        description="None"
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
