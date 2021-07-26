from os import path


class LoadFile:
    def __init__(self):
        print("Loading file")

    @staticmethod
    def Load(Name):  # loads file
        file_name: str = f"Files/{Name}.server"
        if not path.exists(file_name):
            with open(file_name, 'a') as file, open("Files/Settings", 'r') as normal:
                file.write(normal.read())

        with open(file_name, 'r') as file:
            return file.readlines()

    def Info(self, Name, Info):  # get info about setting
        file = self.Load(Name)
        for line in file:
            if line.split(" ")[0] == Info:
                result = line.split(" ")[1]  # check Files/Settings
                return result.rstrip('\n')  # return info

    def Save(self, Name, Info, New):  # save new settings
        file = self.Load(Name)
        text = ""
        for line in file:  # for text
            if line.split(" ")[0] == Info:  # if setting found
                line = f"{Info} {New}"  # replace setting with new setting
            text += line
        file = open(f"Files/{Name}.server", 'w')  # open and write
        file.write(text)
        file.close()

    @staticmethod
    def Test():  # test (just in case)
        print("TEST")
