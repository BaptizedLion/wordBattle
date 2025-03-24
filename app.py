# By Michael
#-----------------------------------------
from flask import Flask, app
app = Flask(__name__)
#-----------------------------------------

# imports all words from english_words library
import random as rand
from english_words import get_english_words_set

allWords = get_english_words_set(['web2'], alpha=True, lower=True)


@app.route('/')
def main():
    # variables
    count = 6
    i = 0
    j = 0
    k = 0
    wordChecker = []


    lettersRemain = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    # files through all words and appends only 4 letter words (the for loop does that below)
    wordList = []

    # creating a list of all four letter words from english_words
    for word in allWords:
        if len(word) == 4:
            wordList.append(word)

    word = rand.choice(wordList)
    while count > 0:
        print('You have ', count, ' attempts left')
        yourWord = input('enter a four letter word: ')
        while len(yourWord) != 4:
            print('enter a valid 4 letter word.')
            yourWord = input('enter a four letter word: ')
        print(yourWord)
        print('comparing words!')
        while i < len(yourWord):
            if yourWord[i] == word[i]:
                wordChecker.append(yourWord[i])
            elif yourWord[i] in word:
                print('the letter(s)', yourWord[i], 'was found in the word but may be in the wrong place')
                wordChecker.append('_')
            else:
                if yourWord[i] in lettersRemain:
                    lettersRemain.remove(yourWord[i])
                wordChecker.append('_')
            i += 1

        print('these letters remain: ', lettersRemain)
        print(wordChecker)
        count -= 1
        # compares your answer to the list
        compare = ''.join(wordChecker)
        if yourWord == compare:
            print('Nice job!')
            break
        if count == 0:
            print('the word was', word)
        else:
            wordChecker.clear()
            i = 0
            # print(wordChecker)

if __name__ == '__main__':
    app.run(debug=True)
