import os
from os import path


class LoadFile:
    def __init__(self):
        print("Loading file")

    @staticmethod
    def Load(Name, user):  # loads file
        if user:
            file_name: str = f"Files/DNA/{Name}.user"
        else:
            file_name: str = f"Files/{Name}.server"
        if not path.exists(file_name):
            if not user:
                with open(file_name, 'a') as file, open("Files/Settings", 'r') as normal:  # noqa
                    file.write(normal.read())
            else:
                with open(file_name, 'a') as file, open("Files/Strands", 'r') as normal:  # noqa
                    file.write(normal.read())

        with open(file_name, 'r') as file:
            return file.readlines()

    def Info(self, Name, Info, user=False):  # get info about setting
        file = self.Load(Name, user)
        if Info == "FILE§":
            return file
        for line in file:
            if line.split(" ")[0] == Info:
                result = line.split(" ")[1]  # check Files/Settings
                return result.rstrip('\n')  # return info

    def Save(self, Name, Info, New, user=False):  # save new settings
        file = self.Load(Name, user)
        if not user:
            text = ""
            for line in file:  # for text
                if line.split(" ")[0] == Info:  # if setting found
                    line = f"{Info} {New}"  # replace setting with new setting
                text += line
            with open(f"Files/{Name}.server", 'w') as file:  # open and write
                file.write(text)
        else:
            text = ""
            for line in file:
                if line.split(" ")[0] == Info:
                    line = f"{Info} {New}\n"
                text += line
            with open(F"Files/DNA/{Name}.user", 'w') as f:
                f.write(text)

    def Del(self, Name, user=False):
        if user:
            os.remove(f"Files/DNA/{Name}.user")
        else:
            os.remove(f"Files/{Name}.server")

    def Check(self, ff1, ff2):
        try:
            if path.samefile(ff1, ff2):
                return True
            return False
        except FileNotFoundError:
            return True

    @staticmethod
    def Test():  # test (just in case)
        print("TEST")
