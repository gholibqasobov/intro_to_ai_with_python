

# print(contents.splitlines())


class Draft:
    def __init__(self):
        filename = 'C:\Python3\Introduction to AI with Python\Lecture 0\src0\maze1.txt'
        try:
            with open(filename) as f:
                contents = f.read()
        except Exception as ex:
            print(ex)

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None

        for i, row in enumerate(self.walls):
            print(i, row)

ex = Draft()
print(ex.print())
