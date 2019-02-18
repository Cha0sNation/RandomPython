#! /home/cha0snation/anaconda3/bin/python

import random


def setup():
    words = ["banana", "apple", "orange", "peach", "grape", "watermelon"]
    output = []
    word = words[random.randint(0, len(words) - 1)]
    playing = True
    tries = 5
    return [words, output, word, tries, playing]


def check_finished(output, tries):
    if tries == 0:
        print("You ran out of tries")
        print()
        return True
    count = 0
    for letter in output:
        if letter != "_":
            count += 1
            if count == len(output):
                print_output(output)
                print()
                print()
                return True
    return False


def check_letter(letter, word, tries):
    correct = False
    for index, letter in enumerate(word):
        if letter == guess:
            output[index] = guess
            correct = True
        if index == len(word) - 1:
            if not correct:
                print("Incorrect guess")
                print()
                return tries - 1
            else:
                return tries


def check_same(guess, output):
    same = False
    for i in output:
        if i == guess:
            same = True
    if same:
        print("You already found that letter")
        print()
        print_output(output)
        print()
        print()
        while True:
            guess = str(input("Guess: "))
            if len(guess) == 1:
                break
        return guess
    else:
        return guess


def print_output(output):
    for i in output:
        print("{0} ".format(i), end="")


if __name__ == "__main__":
    words, output, word, tries, playing = setup()
    while playing:
        print("Try to guess the word:")
        if tries == 1:
            print("You have {0} try left.".format(tries))
        else:
            print("You have {0} tries left.".format(tries))
        # print("DEBUG: word is {0}".format(word))

        if output == []:
            for i in word:
                output.append("_")
            for i in range(len(output)):
                print("_ ", end="")
        else:
            print_output(output)

        print()
        print()

        try:
            while True:
                guess = str(input("Guess: "))
                if len(guess) == 1:
                    break
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except ValueError:
            print("Invalid guess")
            break

        print()

        guess = check_same(guess, output)
        tries = check_letter(guess, word, tries)

        if check_finished(output, tries):
            choice = input("Do you want to play again ? (y or n): ")
            print()
            if choice.lower().startswith("y"):
                words, output, word, tries, playing = setup()
            else:
                playing = False
