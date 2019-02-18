#! /home/cha0snation/anaconda3/bin/python

import random, sys

template_board = {
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

victory_seq = [
    ("top-L", "top-M", "top-R"),
    ("mid-L", "mid-M", "mid-R"),
    ("bot-L", "bot-M", "bot-R"),
    ("top-L", "mid-M", "bot-R"),
    ("top-R", "mid-M", "bot-L"),
    ("top-R", "mid-R", "bot-R"),
    ("top-M", "mid-M", "bot-M"),
    ("top-L", "mid-L", "bot-L"),
]


def print_board(board):
    print(
        """
         {0} | {1} | {2}
        -----------
         {3} | {4} | {5}
        -----------
         {6} | {7} | {8}
        """.format(
            board["top-L"],
            board["top-M"],
            board["top-R"],
            board["mid-L"],
            board["mid-M"],
            board["mid-R"],
            board["bot-L"],
            board["bot-M"],
            board["bot-R"],
        )
    )


def get_symbol():
    while True:
        try:
            playerSymbol = str(input("Do you want to be X or O ?: ")).upper()
            if playerSymbol == "X":
                return [playerSymbol, "O"]
            elif playerSymbol == "O":
                return [playerSymbol, "X"]
            else:
                raise ValueError
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()
        except ValueError:
            print("Invalid choice")


def get_first():
    if random.randint(0, 1):
        print("Player goes first")
        return True
    print("Computer goes first")
    return False


def get_player_move(player_symbol, board):
    while True:
        try:
            player_move = input("Your move (top/mid/bot - L/M/R):")
            if player_move in board and board[player_move] == " ":
                board[player_move] = player_symbol
                print_board(board)
                break
            else:
                print("Invalid move")
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()
        except ValueError:
            print("Invalid choice")

    if not check_finished(board, victory_seq):
        return False
    else:
        return True


def get_computer_move(computer_symbol, player_symbol, board, victory_seq):

    for condition in victory_seq:
        if (
            board[condition[0]] == board[condition[1]] == computer_symbol
            and board[condition[2]] != player_symbol
        ):
            board[condition[2]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        elif (
            board[condition[0]] == board[condition[2]] == computer_symbol
            and board[condition[1]] != player_symbol
        ):
            board[condition[1]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        elif (
            board[condition[1]] == board[condition[2]] == computer_symbol
            and board[condition[0]] != player_symbol
        ):
            board[condition[0]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True

    for condition in victory_seq:
        if (
            board[condition[0]] == board[condition[1]] == player_symbol
            and board[condition[2]] != computer_symbol
        ):
            board[condition[2]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        elif (
            board[condition[0]] == board[condition[2]] == player_symbol
            and board[condition[1]] != computer_symbol
        ):
            board[condition[1]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        elif (
            board[condition[1]] == board[condition[2]] == player_symbol
            and board[condition[0]] != computer_symbol
        ):
            board[condition[0]] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True

    for key in board.keys():
        if (
            key == "top-L" or key == "top-R" or key == "bot-L" or key == "bot-R"
        ) and board[key] == " ":
            board[key] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        else:
            continue
    if board["mid-M"] == " ":
        board["mid-M"] = computer_symbol
        print_board(board)
        if not check_finished(board, victory_seq):
            return False
        else:
            return True
    for key in board.keys():
        if (
            key == "top-M" or key == "mid-L" or key == "mid-R" or key == "bot-M"
        ) and board[key] == " ":
            board[key] = computer_symbol
            print_board(board)
            if not check_finished(board, victory_seq):
                return False
            else:
                return True
        else:
            continue


def check_finished(board, victory_seq):
    for condition in victory_seq:
        if (
            board[condition[0]] == board[condition[1]] == board[condition[2]] == "X"
        ) or (board[condition[0]] == board[condition[1]] == board[condition[2]] == "O"):
            if board[condition[0]] == "O":
                print("The computer won")
            else:
                print("You won")
            board[condition[0]] = board[condition[1]] = board[condition[2]] = "*"
            print_board(board)
            return True
    for cell in board.values():
        if cell == " ":
            return False
    print("It's a tie")
    return True


if __name__ == "__main__":
    print_board(template_board)
    board = template_board.copy()
    player_symbol, computer_symbol = get_symbol()
    if get_first():
        while True:
            # if not finished
            if not get_player_move(player_symbol, board):
                if not get_computer_move(
                    computer_symbol, player_symbol, board, victory_seq
                ):
                    continue
                else:
                    break
            else:
                break
    else:
        while True:
            # if not finished
            if not get_computer_move(
                computer_symbol, player_symbol, board, victory_seq
            ):
                if not get_player_move(player_symbol, board):
                    continue
                else:
                    break
            else:
                break
