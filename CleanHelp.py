import discord


class CleanHelp:
    def __init__(self, client, colour):
        self.client = client
        self.colour = colour
        print("New Help Setup")

    def SetEmbed(self):
        embed = discord.Embed(
            title="Help",
            description="Help with commands",
            colour=self.colour
        )
        return embed

    def makePages(self, pages):
        for cog in self.client.cogs:
            embed = discord.Embed(
                title=f"{cog}",
                description=f"Commands in {cog}",
                colour=self.colour
            )
            for command in self.client.get_cog(cog).get_commands():
                if command.enabled and not command.hidden:
                    embed.add_field(
                        name=f"{command.name} {command.aliases} ({command.description})",  # noqa
                        value=f"Help: {command.help}"
                    )
            embed.set_footer(
                text="[] = aliases,\n" +
                     "() = arguments (inputs)"
            )
            if str(embed.fields) != str([]):
                pages.append(embed)

        self.pages = pages
        return self.pages
