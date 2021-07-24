# import discord
from datetime import datetime as d
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):  # init this script
        self.client = client

    @commands.command(  # commands.command instead of client.command
        # same things can be put here though
        name="Ping",
        description="Check your ping wiht the bot",
        aliases=["ping", "Ping!"]
    )
    async def _Ping(self, ctx):  # requires self as in class
        # returns the ping
        # NOTE: this is from old code that i have so there might be a better version.  # noqa
        # and we are in a cog so. if you find a better way, please replace this

        start = d.timestamp(d.now())
        msg = await ctx.send(content='Pinging')
        await msg.edit(content=f'That took {round(( d.timestamp( d.now() ) - start ) * 1000) }ms') # noqa


# setups the cog for use.
def setup(client):
    client.add_cog(Test(client))
