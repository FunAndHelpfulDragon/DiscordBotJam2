import discord
import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import Load  # noqa E402
Lo = Load.LoadFile()


class Generation:
    def __init__(self, user):
        self.user = user

    def GetInfo(self, author):  # checks if they have a dna already
        if Lo.Check(f"Files/DNA/{author.id}.user", "Dna/Stats"):
            return None
        return True

    def DelGame(self, author):  # gives new game
        Lo.Del(author.id, True)
        return True

    def Random(self, author, number):  # gives user number of strands (to start with)  # noqa
        # loads Strands
        Temp = []
        with open("DNA/Stats", 'r') as Stats:
            file = Stats.readlines()
            while len(Temp) < 7:
                result = random.randint(0, len(file) - 1)
                try:
                    Temp.index(file[result].rstrip('\n'))
                except ValueError:
                    Temp.append(file[result].rstrip('\n'))

        Lo.Save(author.id, 'Inventory', str(Temp).replace(" ", ""), True)

    def Inv(self, author, Option, sss=False):
        if Option is None:
            Option = "Inventory"
        print(Option)
        Inv = Lo.Info(author.id, Option, True)
        Lnv = Inv.split(",")
        Temp = []
        for s in Lnv:
            s1 = s.replace("'", "")
            s1 = s1.replace("[", "")
            s1 = s1.replace("]", "")
            print(s1)
            print(s)
            print(Lnv)
            if not sss:
                if s1 != "":
                    Temp.append(s1)
            else:
                Temp.append(s1)

        print(Temp)
        return Temp

    def LoadInv(self, author, Option=None):
        Temp = self.Inv(author, Option)
        Temp2 = self.Inv(author, Option, True)
        if Option is None:
            Option = "Inventory"

        if Option == "Inventory":
            option = f"Inventory - {len(Temp)} Items"
        elif Option == "Strands":
            option = f"{Option} \nYou have {len(Temp)}/{10} max alvalible of {Option}"  # noqa
        print(option)
        embed = discord.Embed(
            name=option,
            title=option,
            descript=f"Your {option}",
            colour=discord.Colour.random()
        )
        print(Temp)
        if str(Temp) == str([]):
            print("a")
            embed.add_field(
                name="Oh, Oh",
                value="Seems like you haven't put any strands in your dna yet, use `COMMAND` to add some!"  # noqa
            )
        else:
            print("b")
            for Strand in Temp2:
                if Strand != "":
                    Strand = Strand.replace("'", "")
                    Strand = Strand.replace("[", "")
                    Strand = Strand.replace("]", "")
                    embed.add_field(
                        name=f"{Strand} (Pos:{int(Temp2.index(Strand)) + 1})",
                        value="Unknown",
                        inline=False
                    )
        embed.set_footer(
            text=f"{author.name}'s {Option}"
        )
        return embed

    def addInv(self, author, Colour, Position):
        Position = int(Position) - 1
        print("---")
        S = self.Inv(author, 'Strands', True)
        Inv = self.Inv(author, 'Inventory', True)
        print("-")
        print(S)
        if S[Position] == "":
            S[Position] = Colour
            print(S)
            C = str(S).replace(" ", "")
            Lo.Save(author.id, 'Strands', C, True)
            Inv.index(Colour) == ""
            Inv = str(Inv).replace(" ", "")
            Lo.Save(author.id, 'Inventory', Inv, True)
            print("---")
        else:
            return

    def RmInv(self, author, Position):
        Position = int(Position) - 1
        print("---")
        S = self.Inv(author, 'Strands', True)
        Inv = self.Inv(author, 'Inventory', True)
        print("-")
        good = True
        for X in range(0, len(Inv)):
            if not Inv[X]:
                print(X)
                Inv[X] = S[Position]
                S[Position] = ""
                good = False
        if good:
            Inv.append(S[Position])
            S[Position] = ""

        S = str(S).replace(" ", "")
        Lo.Save(author.id, 'Strands', S, True)
        Inv = str(Inv).replace(" ", "")
        Lo.Save(author.id, 'Inventory', Inv, True)
