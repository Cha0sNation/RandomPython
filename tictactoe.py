#! /home/cha0snation/anaconda3/bin/python

import random, sys

TEMPLATE_BOARD = {
    "top-L": " ",
    "top-M": " ",
    "top-R": " ",
    "mid-L": " ",
    "mid-M": " ",
    "mid-R": " ",
    "bot-L": " ",
    "bot-M": " ",
    "bot-R": " ",
}

VICTORY_SEQ = [
    ("top-L", "top-M", "top-R"),
    ("mid-L", "mid-M", "mid-R"),
    ("bot-L", "bot-M", "bot-R"),
    ("top-L", "mid-M", "bot-R"),
    ("top-R", "mid-M", "bot-L"),
    ("top-R", "mid-R", "bot-R"),
    ("top-M", "mid-M", "bot-M"),
    ("top-L", "mid-L", "bot-L"),
]


def print_board(BOARD):
    print(
        """
         {0} | {1} | {2}
        -----------
         {3} | {4} | {5}
        -----------
         {6} | {7} | {8}
        """.format(
            BOARD["top-L"],
            BOARD["top-M"],
            BOARD["top-R"],
            BOARD["mid-L"],
            BOARD["mid-M"],
            BOARD["mid-R"],
            BOARD["bot-L"],
            BOARD["bot-M"],
            BOARD["bot-R"],
        )
    )


def get_symbol():
    while True:
        try:
            PLAYER_SYMBOL = str(input("Do you want to be X or O ?: ")).upper()
            if PLAYER_SYMBOL == "X":
                return [PLAYER_SYMBOL, "O"]
            if PLAYER_SYMBOL == "O":
                return [PLAYER_SYMBOL, "X"]
            raise ValueError
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()
        except ValueError:
            print("Invalid choice")


def get_first():
    if random.randint(0, 1):
        print("Player goes first")
        print()
        return True
    print("Computer goes first")
    print()
    return False


def get_player_move():
    global PLAYER_SYMBOL, BOARD
    while True:
        try:
            player_move = input("Your move (top/mid/bot - L/M/R): ")
            if player_move in BOARD and BOARD[player_move] == " ":
                BOARD[player_move] = PLAYER_SYMBOL
                print("Player's move: ")
                print_board(BOARD)
                break
            else:
                print("Invalid move")
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()
        except ValueError:
            print("Invalid choice")

    if not check_finished():
        return False
    return True


def get_computer_move():
    global COMPUTER_SYMBOL, PLAYER_SYMBOL, BOARD, VICTORY_SEQ
    print("Computer's move: ")
    for condition in VICTORY_SEQ:
        if (
            BOARD[condition[0]] == BOARD[condition[1]] == COMPUTER_SYMBOL
            and BOARD[condition[2]] != PLAYER_SYMBOL
        ):
            BOARD[condition[2]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True
        if (
            BOARD[condition[0]] == BOARD[condition[2]] == COMPUTER_SYMBOL
            and BOARD[condition[1]] != PLAYER_SYMBOL
        ):
            BOARD[condition[1]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True
        if (
            BOARD[condition[1]] == BOARD[condition[2]] == COMPUTER_SYMBOL
            and BOARD[condition[0]] != PLAYER_SYMBOL
        ):
            BOARD[condition[0]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True

    for condition in VICTORY_SEQ:
        if (
            BOARD[condition[0]] == BOARD[condition[1]] == PLAYER_SYMBOL
            and BOARD[condition[2]] != COMPUTER_SYMBOL
        ):
            BOARD[condition[2]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True
        if (
            BOARD[condition[0]] == BOARD[condition[2]] == PLAYER_SYMBOL
            and BOARD[condition[1]] != COMPUTER_SYMBOL
        ):
            BOARD[condition[1]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True
        if (
            BOARD[condition[1]] == BOARD[condition[2]] == PLAYER_SYMBOL
            and BOARD[condition[0]] != COMPUTER_SYMBOL
        ):
            BOARD[condition[0]] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True

    for key in BOARD.keys():
        if key in ("top-L", "top-R", "bot-L", "bot-R") and BOARD[key] == " ":
            BOARD[key] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True

    if BOARD["mid-M"] == " ":
        BOARD["mid-M"] = COMPUTER_SYMBOL
        print_board(BOARD)
        if not check_finished():
            return False
        return True

    for key in BOARD.keys():
        if key in ("top-M", "mid-L", "mid-R", "bot-M") and BOARD[key] == " ":
            BOARD[key] = COMPUTER_SYMBOL
            print_board(BOARD)
            if not check_finished():
                return False
            return True


def check_finished():
    global BOARD, VICTORY_SEQ
    for condition in VICTORY_SEQ:
        if (
            BOARD[condition[0]] == BOARD[condition[1]] == BOARD[condition[2]] == "X"
        ) or (BOARD[condition[0]] == BOARD[condition[1]] == BOARD[condition[2]] == "O"):
            if BOARD[condition[0]] == "O":
                print("The computer won")
            else:
                print("You won")
            BOARD[condition[0]] = BOARD[condition[1]] = BOARD[condition[2]] = "*"
            print_board(BOARD)
            return True
    for cell in BOARD.values():
        if cell == " ":
            return False
    print("It's a tie")
    return True


if __name__ == "__main__":
    print_board(TEMPLATE_BOARD)
    BOARD = TEMPLATE_BOARD.copy()
    PLAYER_SYMBOL, COMPUTER_SYMBOL = get_symbol()
    if get_first():
        while True:
            # if not finished
            if not get_player_move():
                if not get_computer_move():
                    continue
                else:
                    break
            else:
                break
    else:
        while True:
            # if not finished
            if not get_computer_move():
                if not get_player_move():
                    continue
                else:
                    break
            else:
                break
