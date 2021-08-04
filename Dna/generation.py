import discord
import sys
import os
import random
import aiofiles
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import Load  # noqa E402
Lo = Load.LoadFile()


class Generation:
    def __init__(self, user=0):
        # can i change the 'author' in the functions to 'self.user'?
        self.user = user

    def GetInfo(self, author):  # checks if they have a dna already
        if Lo.Check(f"Files/DNA/{author.id}.user", "Dna/Colours"):
            return None
        return True

    def DelGame(self, author):  # gives new game
        Lo.Del(author.id, True)
        return True

    async def Random(self, author, number, save=True, Start=False):  # gives user number of strands (to start with)  # noqa
        # loads Strands
        Temp = []
        async with aiofiles.open("Dna/Colours", 'r') as Colours:
            file = await Colours.readlines()
            if Start:
                Temp.append("red")
                Temp.append("orange")
                Temp.append("purple")
                Temp.append("white")
                Temp.append("black")
            while len(Temp) < number: # makes sure they have atleast number strands to start with (change?)  # noqa
                result = random.randint(0, len(file) - 1)
                try:
                    Temp.index(file[result].rstrip('\n'))
                except ValueError:
                    Temp.append(file[result].rstrip('\n'))

        if save:
            await Lo.Save(author.id, 'Inventory', str(Temp).replace(" ", ""), True)  # noqa
        else:
            return Temp

    async def Inv(self, author, Option, sss=False):  # makes a table of their inventory  # noqa
        if Option is None:  # inventory or strands
            Option = "Inventory"
        if type(author) != int:
            author = author.id
        Inv = await Lo.Info(author, Option, True)  # gets
        Lnv = Inv.split(",")
        Temp = []
        for s in Lnv:  # for Item
            # makes item into a table (easier later)
            s1 = s.replace("'", "")
            s1 = s1.replace("[", "")
            s1 = s1.replace("]", "")
            # the 'sss' makes it so it depends where the items go
            # when 'sss' is false, the items will just be in the table one
            # after another without any gaps. Useful for display items (without
            # caring about position). With 'sss' enabled, it does care about
            # position by adding in "Empty" spaces, these can be useful later
            # when doing things like adding in new dna to a certain position
            if not sss:
                if s1 != "":
                    Temp.append(s1)
            else:
                Temp.append(s1)

        return Temp

    async def LoadInv(self, author, Option=None):
        # loads inventory (twice)
        Temp = await self.Inv(author, Option)
        Temp2 = await self.Inv(author, Option, True)
        # sets the "Option" and "option"
        # Difference:
        # you see 'option' (and 'Option' sometimes),
        # 'Option' is used for making 'option'
        # makes sense?
        if Option is None:
            Option = "Inventory"

        if Option == "Inventory":
            option = f"Inventory - {len(Temp)} Items"
        elif Option == "DNA":
            option = f"{Option} \nYou have {len(Temp)} strands out of {10}  {Option}"  # noqa
        print(option)
        # creates embed
        embed = discord.Embed(
            # name, title both needed?
            name=option,
            title=option,
            descript=f"Your {option}",
            colour=discord.Colour.random()
        )
        if str(Temp) == str([]):  # checks if it's empty
            embed.add_field(
                name="Uh, Oh",
                value="Seems like you haven't got anything in this Inventory"
            )
        else:
            # shows list of strands (and their actrual position)
            for Strand in Temp2:
                if Strand != "":
                    Strand = Strand.replace("'", "")
                    Strand = Strand.replace("[", "")
                    Strand = Strand.replace("]", "")
                    # also, add to embed :)
                    embed.add_field(
                        name=f"{Strand} (Pos:{int(Temp2.index(Strand)) + 1})",
                        value=await self.GetStrandInfo(author.id, Strand),  # didn't have time to do things on this.  # noqa
                        # inline=False
                    )
        # information
        embed.set_footer(
            text=f"{author.name}'s {Option}"
        )
        return embed

    async def addInv(self, author, Colour, Position):
        # takes a colour and position
        # and moves that colour from inventory
        # to position in dna
        Position = int(Position) - 1  # lists start at 1 for the user
        # load invs
        S = await self.Inv(author, 'DNA', True)
        Inv = await self.Inv(author, 'Inventory', True)
        # check if the position is emptys
        # print(S[Position].strip())
        if S[Position] == "":
            S[Position] = Colour  # add colour
            S = str(S).replace(" ", "")  # CONVERTS INTO SAVEABLE FORMAT (spaces make it break)  # noqa
            await Lo.Save(author.id, 'DNA', S, True)
            Pos = Inv.index(Colour)
            Inv[Pos] = ""
            Inv = str(Inv).replace(" ", "")
            await Lo.Save(author.id, 'Inventory', Inv, True)
        else:
            # if, there is an item there already. THe user will be required to
            # remove the item before adding another item.

            # Make this automatic?
            return

    async def RmInv(self, author, Position):
        # takes a item from inputted position and puts it in user inventory
        Position = int(Position) - 1
        S = await self.Inv(author, 'DNA', True)
        Inv = await self.Inv(author, 'Inventory', True)
        good = True
        # attempts to find empty spot
        for X in range(0, len(Inv)):
            if not Inv[X]:
                Inv[X] = S[Position]
                S[Position] = ""
                good = False
        # if no empty spot, add it to the list.
        if good:
            Inv.append(S[Position])
            S[Position] = ""

        S = str(S).replace(" ", "")
        await Lo.Save(author.id, 'DNA', S, True)
        Inv = str(Inv).replace(" ", "")
        await Lo.Save(author.id, 'Inventory', Inv, True)

    def Bot(self, number, Dna):
        # strands = order of strand(S) in dna
        dna = []
        for x in range(0, Dna):  # generates X bots
            dna.append(self.Random("", number, False))  # with random dna
        return dna

    async def GetStrandInfo(self, id, Colour):
        try:
            inv = await self.Inv(id, "unlocked", True)
            async with aiofiles.open("Dna/Stats", 'r') as Stats:
                async with aiofiles.open("Dna/Colours", 'r') as Colours:
                    Color = await Colours.readlines()
                    info = await Stats.readlines()
                    for unlock in inv:
                        unlock = int(unlock)
                        C = Color[unlock].replace(" ", "").rstrip("\n")
                        Colour = Colour.rstrip("\n")
                        if C == Colour:
                            return info[unlock]
        except Exception:
            # print(e)
            return "Unknown"
