class LoadFile():
    def __init__(self):
        print("Loading file")

    def Load(self, Name):  # loads file
        try:
            file = open(f"Files/{Name}.server", 'r')  # trys to find it
        except FileNotFoundError:  # fails and creates
            file = open(f"Files/{Name}.server", 'a')
            normal = open("Files/Settings", 'r')
            file.write(normal.read())
            normal.close()
            file.close()  # can this be better?
            file = open(f"Files/{Name}.server", 'r')
        finally:  # read and return
            r = file.readlines()
            file.close()
            return r

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

    def Test(self):  # test (just in case)
        print("TEST")
