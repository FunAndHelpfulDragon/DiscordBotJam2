import discord
from discord.ext import commands


class Helps(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Help setup")

    @commands.command(
        aliases=['creidt'],
        help="Shows owners of the bot"
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
            value="Programming.",
            inline=True
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=['help'],
        help="HELP! Here is HELP!"
        )
    async def Help(self, ctx):
        Mbeds = []
        for cog in self.client.cogs:
            if cog != "Settings" or ctx.author.permissions_in(ctx.channel).manage_guild:  # noqa
                Tbed = discord.Embed(
                    title=f'{cog} - Info',
                    description=f"Information abouts commands in {cog}",
                    colour=discord.Colour.random()
                )
                for command in self.client.get_cog(cog).get_commands():
                    if command.enabled:
                        Tbed.add_field(
                            name=f"{command.name} {command.aliases}",
                            value=f"Help:{command.help}",
                        )
                if str(Tbed.fields) == str([]):
                    Tbed.add_field(
                        name="Oh, oh!",
                        value="Seems like all the commands in this cog have been disabled."  # noqa
                    )
                Tbed.set_footer(
                    text="[] = aliases"
                )
                Mbeds.append(Tbed)
        for embed in Mbeds:
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['About'],
        help="Shows information about the bot"
    )
    async def about(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="About",
            value="This is a bot made for the discord bot jam 2 (https://itch.io/dbj2) designed by: dragmine149#5048 and Guy_372#4809."  # noqa
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Helps(client))
