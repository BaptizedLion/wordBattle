from flask import Flask, request, jsonify, render_template
import random as rand
from english_words import get_english_words_set

app = Flask(__name__)

# Load words dataset
allWords = get_english_words_set(['web2'], alpha=True, lower=True)
wordList = [word for word in allWords if len(word) == 4]
word = rand.choice(wordList)

# Store guess history
guess_history = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    yourWord = data.get("word", "").lower()

    if len(yourWord) != 4:
        return jsonify({"error": "Please enter a valid 4-letter word."}), 400

    # Improved hint logic
    word_hint = []
    word_copy = list(word)  # Copy to track used letters

    # First pass: mark exact matches
    for i in range(4):
        if yourWord[i] == word[i]:
            word_hint.append(yourWord[i])  # Correct letter & position
            word_copy[i] = None  # Mark as used
        else:
            word_hint.append(None)  # Placeholder

    # Second pass: mark partial matches
    for i in range(4):
        if word_hint[i] is None:  # Not an exact match
            if yourWord[i] in word_copy:
                word_hint[i] = "_"  # In word but wrong position
                word_copy[word_copy.index(yourWord[i])] = None  # Mark as used
            else:
                word_hint[i] = "X"  # Not in word

    # Store this guess in history
    guess_history.append({
        "guess": yourWord,
        "hint": word_hint
    })

    return jsonify({
        "your_guess": yourWord,
        "word_hint": word_hint,
        "guess_history": guess_history
    })


@app.route('/reset', methods=['POST'])
def reset_game():
    global word, guess_history
    word = rand.choice(wordList)
    guess_history = []
    return jsonify({"message": "Game reset with new word"})

@app.route('/get-word')
def get_word():
    return jsonify({'word': word})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)