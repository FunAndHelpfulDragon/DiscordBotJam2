import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.view = False
        self.Change = False

    @commands.command(aliases=['settings', 'SETTINGS'])
    async def Settings(self, ctx, option="None"):
        # option is for if they just want to go straight there
        Prefix = "!"

        def view():  # view settings
            embed = discord.Embed(
                    colour=discord.Colour.red())  # setting to change?
            embed.add_field(
                    name="Settings",
                    value=f"Prefix: {Prefix}",  # better way than putting them all here?  # noqa
                    )
            return embed

        def change():
            print("Changing...")

        if option.lower() == "view":
            await ctx.send(embed=view())
        elif option.lower() == "change":
            change()
        else:
            await ctx.send("What would you like to do (view or change):")

            def check(m):
                if m.content.lower() == "view":
                    self.view = True
                elif m.content.lower() == "change":
                    self.change = True
                return m.channel == ctx.channel

            await self.client.wait_for('message', check=check)

        if self.view:
            await ctx.send(embed=view())
        elif self.change:
            change()

        self.view = False
        self.change = False

    # @commands.command()


def setup(client):
    client.add_cog(Settings(client))
