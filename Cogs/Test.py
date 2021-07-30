import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):  # init this script
        self.client = client

    @commands.command(  # commands.command instead of client.command
        # same things can be put here though
        name="Ping",
        description="None",
        help="Check your ping with the bot",
        aliases=["ping", "Ping!"],
        enabled=True
    )
    async def _Ping(self, ctx):  # requires self as in class
        # returns the ping
        await ctx.send(f"Pong! {self.client.latency*1000}ms") # noqa

    @commands.command(
        enabled=False
    )
    async def THelp(self, ctx):
        # iterating trough cogs
        for cog in self.client.cogs:
            # check if cog is the matching one
            if cog.lower() == "Dna".lower():

                # making title - getting description from doc-string belowclass
                emb = discord.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].__doc__,  # noqa
                                    color=discord.Color.green())

                # getting commands from cog
                for command in self.client.get_cog(cog).get_commands():
                    # if cog is not hidden
                    if not command.hidden:
                        emb.add_field(name=f"`!{command.name}`", value=command.help, inline=False)  # noqa
                # found cog - breaking loop
                break
        await ctx.send(embed=emb)

    @commands.command(
        aliases=['aahelp'],
        help="HELP!",
        enabled=False
        )
    async def TTHelp(self, ctx, Page=None):
        Mbeds = []
        if Page is None:
            for cog in self.client.cogs:
                if cog != "Settings" or ctx.author.permissions_in(ctx.channel).manage_guild:  # noqa
                    Tbed = discord.Embed(
                        title=f'{cog} - Info',
                        description=f"Information abouts commands in {cog}",
                        colour=discord.Colour.random()
                    )
                    for command in self.client.get_cog(cog).get_commands():
                        Tbed.add_field(
                            name=command.name,
                            value=command.help,
                        )
                    Mbeds.append(Tbed)
        for embed in Mbeds:
            await ctx.send(embed=embed)


# setups the cog for use.
def setup(client):
    client.add_cog(Test(client))
