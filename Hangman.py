from nltk.corpus import words
from c_module import c_input as ci  # CUSTOM MODULE: LOOPS INPUT UNTIL VALID ANSWER
import random


def dict_change(word_bank, guess, result, pos):
    """UPDATE WORD BANK BASED ON GUESSES"""
    update = []
    if result is True:  # IF GUESSED CORRECTLY
        for i in word_bank:
            check = 0
            for j in pos:
                if i[j] == guess: check += 1
            if check == len(pos): update.append(i)
    elif result is False:  # IF GUESSED INCORRECTLY
        for i in word_bank:
            update.append(i) if guess not in i else None
    else: exit("Error: dict_change()")
    return update


def word_change(user_word, guess, pos):
    """UPDATE USER WORD WHEN GUESSED CORRECTLY"""
    for i in pos:
        user_word = user_word[:i] + guess + user_word[i + 1:]
    return user_word


def ai_guess(word_bank, user_word, guessed_letters):
    """GUESS A LETTER BASED ON REMAINING WORDS IN WORD BANK"""
    while True:
        guess = word_bank[random.randint(0, len(word_bank) - 1)][user_word.rindex("_")]
        if guess not in guessed_letters: break
    return guess


# INSTRUCTIONS
print("---------------------------------------------------------------------------------------------------\n"
      "Let's play Hangman!\n"
      "\n"
      "Before starting, here are some ground rules for the word you'll choose: \n"
      " - It must not be a name\n"
      " - It must not contain any capital letters\n"
      " - It must not contain any numbers\n"
      " - It must not contain any punctuations such as apostrophes\n"
      "\n"
      "Ok, got all that?")
input("Press enter to continue")

# SETTING UP
dictionary = words.words()
word_bank = []
length = list(range(ci.input_loop("int", "What is the length of your word: ")))
num_guess = ci.input_loop("int", "How many guesses do I get: ")
user_word = "_" * (max(length) + 1)
guessed_letters = []
guessed_wrong = 0
for i in dictionary:
    word_bank.append(i) if len(i) == max(length) + 1 else None


# MAIN LOOP
print("---------------------------------------------------------------------------------------------------")
while num_guess != 0:
    print("I have been wrong " + str(guessed_wrong) + " times and have " + str(num_guess) + " misses left.\n"
          "What I have guessed so far: [" + ", ".join(guessed_letters) + "]\n\n" +
          user_word + "\n")
    exit("Your word does not exist") if len(word_bank) == 0 else None
    guess = ai_guess(word_bank, user_word, guessed_letters)
    guessed_letters += [guess]
    result = ci.input_loop("str", "Does your word contain letter '" + guess + "' (y/n): ", ["Y", "y", "N", "n"])
    pos = []
    if result in ["Y", "y"]:  # IF CORRECTLY GUESSED
        result = True
        occurrence = ci.input_loop("int", "How many often does the letter '" + guess + "' appear in your word: ",
                                   list(range(1, max(length) + 2)))
        for i in range(occurrence):
            pos += [ci.input_loop("int", "Enter a position of '" + guess + "': ", list(range(1, max(length) + 2))) - 1]
        user_word = word_change(user_word, guess, pos)
        if "_" not in user_word:  # WIN CONDITION: AI GUESSED ALL THE WORDS
            print("---------------------------------------------------------------------------------------------------")
            break
    elif result in ["N", "n"]:
        result = False
        guessed_wrong += 1
    else: exit("Error: result")
    word_bank = dict_change(word_bank, guess, result, pos)
    num_guess -= 1
    print("---------------------------------------------------------------------------------------------------")
win = False if num_guess == 0 else True
print("Your word is '" + user_word + "'\nYay, I've won!") if win is True else print\
     ("I have ran out of guesses\nCongratulations, you have won!")
exit()
