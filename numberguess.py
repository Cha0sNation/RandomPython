#! /home/cha0snation/anaconda3/bin/python

import random


def check_guess():
    global GUESS, NUMBER, TRIES, PLAYING
    # pylint: disable=used-before-assignment
    if GUESS == NUMBER:
        print("You guessed correctly.")
        print()
        again = input("Try again (y/n): ")
        print()
        if not again.lower().startswith("y"):
            PLAYING = False
        else:
            TRIES = 6
            NUMBER = random.randint(1, 10)
    else:
        print("You guessed incorrectly, ", end="")
        TRIES -= 1
        if GUESS > NUMBER:
            print("your guess is too big.")
            print()
        else:
            print("your guess is too small.")
            print()


if __name__ == "__main__":
    NUMBER = random.randint(1, 10)
    TRIES = 6
    PLAYING = True
    while TRIES > 0 and PLAYING:
        try:
            GUESS = int(input("Guess a number (from 1-10): "))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except ValueError:
            print("Invalid number")
            break
        check_guess()
        if TRIES == 0:
            print("You failed to guess correctly")
            print("The correct number was {0}".format(NUMBER))
            break
        if PLAYING:
            print("You have {0} tries left".format(TRIES))
