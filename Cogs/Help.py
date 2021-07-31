import discord
from discord.ext import commands


class Helps(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Help setup")

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

    @commands.command(
        aliases=['help'],
        help="HELP! Here is HELP!",
        description="(Optional: Cog)"
        )
    async def Help(self, ctx, Additions=""):
        Mbeds = []
        if Additions.lower() == "settings":  # information about settings
            if ctx.author.permissions_in(ctx.channel).manage_guild:
                embed = discord.Embed(
                    title="Settings help",
                    description="Information about settings",
                    colour=discord.Colour.random()
                )
                embed.add_field(
                    name="Prefix",
                    value="Changes the prefix of the server, accepted prefix, anything."  # noqa
                )
                embed.add_field(
                    name="Notifications",
                    value="Set a channel to get notifications from the bot, These notifications will rarley happen. Accepted: off, channel_id"  # noqa
                )
                await ctx.send(embed=embed)
        elif Additions.lower() == "colour":  # information about colours and category colours go under.  # noqa
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
        else:
            for cog in self.client.cogs:  # all cogs
                # check if user has permission to view that cog
                if cog != "Settings" or ctx.author.permissions_in(ctx.channel).manage_guild:  # noqa
                    Tbed = discord.Embed(
                        title=f'{cog} - Info',
                        description=f"Information abouts commands in {cog}",
                        colour=discord.Colour.random()
                    )
                    # for command in cog
                    for command in self.client.get_cog(cog).get_commands():
                        if command.enabled:  # checks if enabled (there are some disabled)  # noqa
                            Tbed.add_field(
                                name=f"{command.name} {command.aliases} ({command.description})",  # name, aliases (would also be nice for auto other (required/not) options)  # noqa
                                value=f"Help: {command.help}",  # help
                            )
                    if str(Tbed.fields) == str([]):  # checks if no field
                        Tbed.add_field(
                            name="Oh, oh!",
                            value="Seems like all the commands in this cog have been disabled."  # noqa
                        )
                    Tbed.set_footer(  # help (info)
                        text="[] = aliases,\n" +
                             "() = arguments (inputs)"
                    )
                    Mbeds.append(Tbed)
            for embed in Mbeds:  # send all embeds
                await ctx.send(embed=embed)

    @commands.command(
        aliases=['About'],
        help="Shows information about the bot",
        description="None"
    )
    async def about(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.random()
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


def setup(client):
    client.add_cog(Helps(client))
