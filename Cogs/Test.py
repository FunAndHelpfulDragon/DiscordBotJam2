# import discord
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
        await ctx.send(f"Pong! {self.client.latency*1000}ms") # noqa


# setups the cog for use.
def setup(client):
    client.add_cog(Test(client))
