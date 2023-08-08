from random import randint 

# reading words file  
with open('words.txt') as f:
    word = f.readlines()  

# chooses a random word
randomWord = word[randint(0, len(word))]
f.close()

win = False
# validates user input to see if its a valid choice
def getUserInput():
    userGuess = input("Please enter a 5 letter english word..").replace(" ", "")
    if len(userGuess) != 5:
        userGuess = input("Please enter a 5 letter english word..")
    elif userGuess.isnumeric():
        userGuess = input("Please enter a 5 letter english word..")
    return userGuess
print("correct word:", randomWord)

# checks the user guess and the random word
def validateGuess(guess, correctWord):
    # removes the \n from the end b/c of the .txt
    correctWord = correctWord.strip()
    guessDict = {}
    correctWordDict = {}
    # setting dictionaries
    for count,i in enumerate(guess):
        guessDict[count] = i

    for count, i in enumerate(correctWord):
        correctWordDict[count] = i
     
    # changing win condition
    if(guessDict == correctWordDict):
        # setting this global so we can use it in our game logic
        global win
        win = True
        
    for index in range(5):
        # check if word is the same position
        if correctWordDict[index] == guessDict[index]:
            print(correctWordDict[index], end="")
            # deletion- so if the letter repeats twice in the guess the second letter
            # isnt confused with the first letter that was correct. ex: bombe & bombb 
            del correctWordDict[index]
            del guessDict[index]
        # check if word is in the dictionary
        elif guessDict[index] in correctWordDict.values():
            # for the yellow _ effect 
            print("\033[33mhello\033[0m", end="") 
        # if letter not in word, its empty
        else:
            print("_", end="")

guesses = 5
# game logic
while(guesses > 0):
    validateGuess(getUserInput(), randomWord)
    if win == True:
        print("\nYou have won.")
        break
    guesses -= 1
    print(f"\nYou have {guesses} guesses left")
    if guesses == 0:
        print("Sorry you have lost :(")

        