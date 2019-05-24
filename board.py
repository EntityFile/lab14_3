import copy
import random
from linked_binary_tree import LinkedBinaryTree


def generate_winning_combinations():
    combinations = []
    for i in range(3):
        combination1 = []
        combination2 = []
        for j in range(3):
            combination1.append((i, j))
            combination2.append((j, i))
        combinations.append(combination1)
        combinations.append(combination2)

    combinations.append([(0, 0), (1, 1), (2, 2)])
    combinations.append([(0, 2), (1, 1), (2, 0)])
    return combinations


class Board:
    NOUGHT = 1
    CROSS = -1
    EMPTY = 0

    NOUGHT_WINNER = 1
    CROSS_WINNER = -1
    DRAW = 2
    NOT_FINISHED = 0

    WINNING_COMBINATIONS = generate_winning_combinations()

    def __init__(self):
        self.cells = [[0] * 3 for _ in range(3)]
        self.last_move = Board.NOUGHT
        self.number_of_moves = 0
        self.status = None
        self.tree = LinkedBinaryTree(self)

    def make_move(self, cell):
        if self.cells[cell[0]][cell[1]] != 0:
            return False
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def has_winner(self):
        for combination in self.WINNING_COMBINATIONS:
            lst = []
            for cell in combination:
                lst.append(self.cells[cell[0]][cell[1]])
            if max(lst) == min(lst) and max(lst) != Board.EMPTY:
                return max(lst)
        if self.number_of_moves == 9:
            return Board.DRAW

        return Board.NOT_FINISHED

    def make_random_move(self):
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == Board.EMPTY:
                    possible_moves.append((i, j))
        cell = random.choice(possible_moves)
        self.last_move = -self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def compute_score(self, board, turn):
        has_winner = board.has_winner()
        if has_winner:
            winner_scores = {Board.NOUGHT_WINNER: 1, Board.CROSS_WINNER: -1, Board.DRAW: 0}
            return winner_scores[has_winner]
        left_board = copy.deepcopy(board)
        right_board = copy.deepcopy(board)
        if turn:
            left_board.make_random_move()
            right_board.make_random_move()

        return left_board.compute_score(left_board, 1) + right_board.compute_score(right_board, 1)

    def compute_turn(self):
        has_winner = self.has_winner()
        if has_winner:
            winner_scores = {Board.NOUGHT_WINNER: 1, Board.CROSS_WINNER: -1, Board.DRAW: 0}
            return winner_scores[has_winner]
        left_board = copy.deepcopy(self)
        right_board = copy.deepcopy(self)
        left_board.make_random_move()
        right_board.make_random_move()
        first = self.compute_score(left_board, 0)
        second = self.compute_score(right_board, 0)

        if first > second:
            self.cells = left_board.cells
            self.last_move = left_board.last_move
            self.number_of_moves = left_board.number_of_moves
        else:
            self.cells = right_board.cells
            self.last_move = right_board.last_move
            self.number_of_moves = right_board.number_of_moves

    def update_tree(self):
        self.tree.key = self

    def __str__(self):
        transform = {0: " ", 1: "O", -1: "X"}
        return "\n".join([" ".join(map(lambda x: transform[x], row)) for row in self.cells])


if __name__ == "__main__":
    board1 = Board()
    while True:
        if board1.has_winner() == 1:
            print('Computer wins!')
            a = input('Again?(y/n): ')
            if a == 'n':
                break
            else:
                board1 = Board()
        elif board1.has_winner() == -1:
            print('Player wins!')
            a = input('Again?(y/n): ')
            if a == 'n':
                break
            else:
                board1 = Board()
        elif board1.has_winner() == 2:
            print('Draw!')
            a = input('Again?(y/n): ')
            if a == 'n':
                break
            else:
                board1 = Board()
        answer = input('Type cords (example: 1 1): ').split()
        answer = [int(num) for num in answer]
        board1.make_move(answer)
        print(board1)
        print()
        board1.compute_turn()
        print('Computer:\n',board1)
        print()

