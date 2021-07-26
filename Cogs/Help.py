import discord
from discord.ext import commands


class Helps(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Help setup")

    @commands.command(aliases=['creidt'])
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
        # embed.add_field(
        #     name="Guy_732#4809",
        #     value="Programming.",
        #     inline=True
        # )
        await ctx.send(embed=embed)

    @commands.command(aliases=['help'])
    async def Help(self, ctx, Category=None):
        embed = discord.Embed(
            name="Help",
            description="Need help? Come here!",
            colour=discord.Colour.random()
        )

        def NoPerm(embed):
            embed.add_field(
                name="Category: Help",
                value="Help: this command \n" +
                      "Credit: people who worked on this bot \n" +
                      "About: about this bot"
            )
            embed.add_field(
                name="Category: Test",
                value="Ping: get your ping to the bot."
            )
            return embed

        def AdminPerm(embed):
            embed.add_field(
                name="Category: Settings",
                value="Settings: change settings for the bot"
            )
            return embed

        def BotOwner(embed):
            embed.add_field(
                name="Category: Main",
                value="Load: loads a cog \n" +
                      "Unload: unloads a cog \n" +
                      "Reload: reloads cogs \n" +
                      "ListCogs: list alvalible cogs"
            )
            return embed

        if Category is None:
            embed = NoPerm(embed)
            if ctx.author.permissions_in(ctx.channel).administrator:
                embed = AdminPerm(embed)
            if ctx.author.id == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
                embed = BotOwner(embed)

            embed.set_footer(text="Want more help? use the help command with a Category!")  # noqa

            await ctx.send(embed=embed)
        else:
            if Category.lower() == "main":
                if ctx.author.id == 467718535897022479 or ctx.author.id == 673573452694945862:  # noqa
                    embed.add_field(
                        name="Load {load} <Cog Name>",
                        value="Loads a cog"
                    )
                    embed.add_field(
                        name="Unload {UnLoad, unload} <Cog Name>",
                        value="unloads a cog"
                    )
                    embed.add_field(
                        name="Reload {reload} [Cog Name]",
                        value="reloads a cog(s)"
                    )
                    embed.add_field(
                        name="ListCogs {List}",
                        value="List all cogs"
                    )
            elif Category.lower() == "settings":
                if ctx.author.permissions_in(ctx.channel).manage_guild:
                    embed.add_field(
                        name="Settings {settings, SETTINGS}, [Option]",
                        value="view or change settings."
                    )
            elif Category.lower() == "help":
                embed.add_field(
                    name="Help [Category]",
                    value="Help?"
                )
                embed.add_field(
                    name="Credit",
                    value="Shows Credits"
                )
            elif Category.lower() == "test":
                embed.add_field(
                    name="Ping",
                    value="Shows your ping to the bot."
                )
            embed.set_footer(text="Usage:\n" +
                                  "{} = aliases (another way of using command) \n" +  # noqa
                                  "<> = Required \n" +
                                  "[] = Optional")
            await ctx.send(embed=embed)

    @commands.command(aliases=['About'])
    async def about(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.random()
        )
        embed.add_field(
            name="About",
            value="This is a bot made for the discord bot jam 2 (https://itch.io/dbj2) designed by: dragmine149#5048"  # and Guy_372#4809."  # noqa
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Helps(client))
