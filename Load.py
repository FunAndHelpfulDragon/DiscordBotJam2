import os
import aiofiles
from os import path


class LoadFile:
    def __init__(self):
        print("Loading file")

    @staticmethod
    def Load(Name, user):  # loads file
        if user:
            file_name: str = f"Files/DNA/{Name}.user"  # dna
        else:
            file_name: str = f"Files/{Name}.server"
        if not path.exists(file_name):
            if not user:
                async with aiofiles.open(file_name, 'a') as file, aiofiles.open("Files/Settings", 'r') as normal:  # noqa
                    await file.write(await normal.read())
            else:
                async with aiofiles.open(file_name, 'a') as file, aiofiles.open("Files/Strands", 'r') as normal:  # noqa
                    await file.write(await normal.read())

        async with aiofiles.open(file_name, 'r') as file:
            return await file.readlines()

    def Info(self, Name, Info, user=False):  # get info about setting
        file = self.Load(Name, user)
        for line in file:
            if line.split(" ")[0].lower() == Info.lower():
                result = line.split(" ")[1]  # check Files/Settings
                return result.rstrip('\n')  # return info

    def Save(self, Name, Info, New, user=False):  # save new settings
        print(Name, Info, New, user)
        file = self.Load(Name, user)
        if not user:
            text = ""
            print(file)
            for line in file:  # for text
                if line.split(" ")[0].lower() == Info.lower():  # if setting found  # noqa
                    line = f"{Info} {New}\n"  # replace setting with new settin
                text += line
            async with aiofiles.open(f"Files/{Name}.server", 'w') as file:
                print(text)
                await file.write(text)
        else:  # dna saving, same thing different dir. Combine?
            text = ""
            for line in file:
                if line.split(" ")[0].lower() == Info.lower():
                    line = f"{Info} {New}\n"
                text += line
            async with aiofiles.open(F"Files/DNA/{Name}.user", 'w') as f:
                await f.write(text)

    def Del(self, Name, user=False):  # delete file
        if user:
            os.remove(f"Files/DNA/{Name}.user")
        else:
            os.remove(f"Files/{Name}.server")

    def Check(self, ff1, ff2):  # check if 2 files have the same content
        try:
            if path.samefile(ff1, ff2):
                return True
            return False
        except FileNotFoundError:
            return True

    @staticmethod
    def Test():  # test (just in case)
        print("TEST")
