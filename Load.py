class LoadFile():
    def __init__(self):
        print("Loading file")

    def Load(self, Name):
        try:
            file = open(f"Files/{Name}.server", 'r')
        except FileNotFoundError:
            file = open(f"Files/{Name}.server", 'a')
            normal = open("Files/Settings", 'r')
            file.write(normal.read())
            normal.close()
            file.close()
            file = open(f"Files/{Name}.server", 'r')
        finally:
            r = file.readlines()
            file.close()
            return r

    def Info(self, Name, Info):
        file = self.Load(Name)
        for line in file:
            if line.split(" ")[0] == Info:
                result = line.split(" ")[1]
                return result

    def Save(self, Name, Info, New):
        file = self.Load(Name)
        text = ""
        for line in file:
            print(line.split(" ")[0] == Info)
            if line.split(" ")[0] == Info:
                line = f"{Info} {New}"
            text += line
        file = open(f"Files/{Name}.server", 'w')
        file.write(text)
        file.close()

    def Test(self):
        print("TEST")
