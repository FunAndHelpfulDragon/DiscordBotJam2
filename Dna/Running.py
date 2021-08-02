import sys
import os
import generation as gen
import random
import aiofiles
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import Load  # noqa E402
Lo = Load.LoadFile()
g = gen.Generation()


class Running:
    def __init__(self):
        print("Running Sim Class started")
        # TODO:
        # make bot generate X copies with random DNA
        # use stats and math and stuff to generate distance
        # in Y time.
        # Punish/reward user.
        # Regenerate new ai with better dna.

    async def Info(self, author, score):
        Y = score[0]
        score.sort()
        if score.index(Y) > (len(score)/2):  # upper half
            inv = await g.Inv(author, "Inventory", True)
            stra = await g.Inv(author, 'DNA', True)
            option = g.Random("", 1, False)
            max = 1
            option[0] = option[0].replace(" ", "")
            unique = []
            for i in inv:
                unique.append(i)
            for i in stra:
                unique.append(i)
            unique = list(filter(None, unique))
            while option[0] in inv or option[0] in stra:
                option = g.Random("", 1, False)
                option[0] = option[0].replace(" ", "")
                max += 1
                if option[0] not in unique:
                    unique.append(option[0])
                if len(unique) >= 30:  # need to change value.
                    return "Max", ""
            s = str(option[0])
            inv.append(s)
            if inv[0] == "":
                del inv[0]
                for x in range(len(inv), 10):
                    inv.append('')
            ninv = str(inv).replace(" ", "")
            await Lo.Save(author.id, 'Inventory', ninv, True)
            return "New Item", s
        elif score.index(Y) == len(score):  # lower half
            inv = await g.Inv(author, "Inventory", True)
            rr = random.randint(0, len(inv))
            rrr = inv[rr]
            if inv.count(inv[0]) == len(inv):
                del inv[rr]
                strinv = str(inv)
                strinv = strinv.replace(" ", "")
                await Lo.Save(author.id, 'Inventory', strinv, True)
            else:
                inv = await g.Inv(author, "DNA", True)
                del inv[rr]
                strinv = str(inv)
                strinv = strinv.replace(" ", "")
                await Lo.Save(author.id, 'DNA', strinv, True)
            return "Loss", rrr
        else:
            return "None", ""

    async def Sim(self, id, random=False):
        info = await g.Inv(id, "DNA", True)
        # if random:
        #     strand = g.Random("", 1, False)
        #     # pdb.set_trace()
        #     while strand[0].replace(" ", "") in info:
        #         # pdb.set_trace()
        #         strand = g.Random("", 1, False)
        #     # s = str(strand[0])
        #     s = strand[0].replace(" ", "")
        #     info.append(s)
        if random:
            info = g.Random("", len(info), False)
        results = []
        results = await self.Stats(info)
        Score = []
        re = self.Run(results)
        Score.append(re)
        return Score

    def Run(self, bot):
        # Speed = distance
        # energy = Time
        # Nodes = Ability (no nodes, and you can't move)
        # Nu = nothing. seriously nothing
        Time = 0  # seconds
        Speed = 0  # mph
        Nodes = 0  # brains (legs)
        Nu = 0  # nothing nodes, (less score?)
        for Stat in bot:
            Sinfo = Stat[1]
            operation = 0
            if Sinfo.find("+") >= 0:
                operation = 0
                Sinfo = Sinfo.split("+")
            elif Sinfo.find("-") >= 0:
                operation = 1
                Sinfo = Sinfo.split("-")
            elif Sinfo.find("x") >= 0:
                operation = 2
                Sinfo = Sinfo.split("x")
            else:
                print("WARNING: Sinfo didn't return correct value!")

            if Stat[0] == "S":
                if operation == 0:
                    Speed += int(Sinfo[1])
                elif operation == 1:
                    Speed -= int(Sinfo[1])
                elif operation == 2:
                    Speed *= int(Sinfo[1])
            if Stat[0] == "E":
                if operation == 0:
                    Time += int(Sinfo[1])
                elif operation == 1:
                    Time -= int(Sinfo[1])
                elif operation == 2:
                    Time *= int(Sinfo[1])
            if Stat[0] == "N":
                if operation == 0:
                    Nodes += int(Sinfo[1])
                elif operation == 1:
                    Nodes -= int(Sinfo[1])
                elif operation == 2:
                    Nodes *= int(Sinfo[1])  # x2 speed.
            if Stat[0] == "Nu":
                if operation == 0:
                    Nu += int(Sinfo[1])
                elif operation == 1:
                    Nu -= int(Sinfo[1])
                elif operation == 2:
                    Nu *= int(Sinfo[1])

        if Nodes <= 0:  # no nodes, can't do anything (like no brain)
            return 0
        else:
            if Time == 0:   # no time, you don't have Energy
                return 0
            else:
                Result = 0
                Speed = Speed / 3600
                Result = Speed * Time
                Result = Result * (Nodes/2)
                Result = Result * 100  # POSITIVE
                return round(Result, 5)
                # return Result
            # simulation (math basically) starts here

    @staticmethod
    async def Stats(self, bot):
        StatTable = []
        async with aiofiles.open("./Dna/Stats", 'r') as s:
            async with aiofiles.open("./Dna/Colours", 'r') as c:
                colours = await c.readlines()
                info = await s.readlines()
                for strand in bot:
                    if strand.strip():  # checks if it is not equal to ''
                        lines = 0  # can this be better?
                        for line in colours:
                            line = line.replace(" ", "")
                            strand = strand.replace(" ", "")
                            if str(strand).rstrip('\n') == str(line).rstrip('\n'):  # noqa
                                binfo = info[lines]
                                ainfo = binfo.split(" ")
                                newinfo = [ainfo[0].rstrip('\n'), ainfo[1].rstrip('\n')]  # noqa
                                if newinfo not in StatTable:
                                    StatTable.append(newinfo)  # noqa
                                    break
                            lines += 1
        return StatTable
