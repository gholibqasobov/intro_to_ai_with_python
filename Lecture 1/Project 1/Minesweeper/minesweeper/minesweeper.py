import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells) and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        """1) mark the cell as a move that has been made"""
        self.moves_made.add(cell)

        """2) mark the cell as safe"""
        self.mark_safe(cell)

        """3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`"""
        sentence_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Ignore the cell in safes
                if (i, j) in self.safes:
                    continue

                # Ignore the cell in mines
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # Add cell to the set
                if 0 <= i < self.height and 0 <= j < self.width:
                    sentence_cells.add((i, j))
        # Add the set of cells and count to knowledge base
        self.knowledge.append(Sentence(sentence_cells, count))

        """4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base"""
        """Iteratively mark guaranteed safes and mines, and infer new knowledge"""

        changed_knowledge = True
        while changed_knowledge:
            changed_knowledge = False
            safes = set()
            mines = set()
            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

            if safes:
                changed_knowledge = True
                for safe in safes:
                    self.mark_safe(safe)

            if mines:
                changed_knowledge = True
                for mine in mines:
                    self.mark_mine(mine)

            self.knowledge[:] = [sentence for sentence in self.knowledge if sentence != Sentence(set(), 0)]

            for sentence_1 in self.knowledge:
                for sentence_2 in self.knowledge:
                    if sentence_1.cells == sentence_2.cells:
                        continue

                    if sentence_1.cells == set() and sentence_1.count > 0:
                        raise ValueError

                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_sentence_cells = sentence_2.cells - sentence_1.cells
                        new_count = sentence_2.count - sentence_1.count

                        new_sentence = Sentence(new_sentence_cells, new_count)

                        if new_sentence not in self.knowledge:
                            changed_knowledge = True
                            self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made

        if safe_moves:
            return random.choice(list(safe_moves))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        MINES = 8
        moves = dict()

        """How are we going to make a random move. 
        Based on the probability of mines in the cell.
        
        basic probability is equal to number of mines left and spaces left
        """
        mines_left = MINES - len(self.mines)
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))
        if spaces_left == 0:
            return None
        basic_prob = mines_left/spaces_left

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moves[(i, j)] = basic_prob

        # if knowledge base is empty meaning the first move
        if moves and not self.knowledge:
            moves_list = list(moves.keys())
            return random.choice(moves_list)
        elif moves and self.knowledge:
            # define mine probability
            # mine_prob = count/cell_num
            for sentence in self.knowledge:
                cell_num = len(sentence.cells)
                count = sentence.count
                mine_prob = count/cell_num
                for cell in sentence.cells:
                    if moves[cell] < mine_prob:
                        moves[cell] = mine_prob

            move_list = [[x, moves[x]] for x in moves]
            move_list.sort(key=lambda x: x[1])
            best_prob = move_list[0][1]

            best_moves = [x for x in move_list if x[1] == best_prob]

            move = random.choice(best_moves)[0]
            return move
