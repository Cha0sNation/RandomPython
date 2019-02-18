#! /home/cha0snation/anaconda3/bin/python

import random


def check_guess(guess, number, tries, playing):
    if guess == number:
        print("You guessed correctly.")
        print()
        again = input("Try again (y/n): ")
        print()
        if not again.lower().startswith("y"):
            playing = False
    else:
        print("You guessed incorrectly, ", end="")
        tries -= 1
        if guess > number:
            print("your guess is too big.")
            print()
        else:
            print("your guess is too small.")
            print()


if __name__ == "__main__":
    number = random.randint(1, 10)
    tries = 6
    playing = True
    while tries > 0 and playing:
        try:
            guess = int(input("Guess a number (from 1-10): "))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except ValueError:
            print("Invalid number")
            break
        check_guess(guess, number, tries, playing)
        if tries == 0:
            print("You failed to guess correctly")
            print("The correct number was {0}".format(number))
            break
        print("You have {0} tries left".format(tries))
