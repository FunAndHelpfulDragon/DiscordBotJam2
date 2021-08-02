import discord


class CleanHelp:
    def __init__(self, client, colour):
        self.client = client
        self.colour = colour
        print("New Help Setup")

    def makePages(self, pages):
        for cog in self.client.cogs:
            embed = discord.Embed(  # new embed
                title=f"{cog}",
                # description=f"{cog.description}",
                colour=self.colour
            )
            for command in self.client.get_cog(cog).get_commands():  # get commands  # noqa
                if command.enabled and not command.hidden:
                    embed.add_field(
                        name=f"{command.name} {command.aliases} ({command.description})",  # noqa
                        value=f"Help: {command.help},\n" +
                              f"Usage: {command.usage}"
                    )
            embed.set_footer(  # info
                text="[] = aliases,\n" +
                     "() = arguments (inputs)"
            )
            if str(embed.fields) != str([]):
                pages.append(embed)

        return pages  # return
