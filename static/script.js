function sendGuess() {
    const word = document.getElementById("wordInput").value;

    if (word.length !== 4) {
        document.getElementById("result").innerText = "Please enter a 4-letter word";
        return;
    }

    fetch("/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ word: word })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerText = data.error;
        } else {
            document.getElementById("result").innerText = `You guessed: ${data.your_guess}`;
            updateHints(data.guess_history);

            // Check if the guess is correct
            if (data.word_hint.every(letter => letter !== "_" && letter !== "X")) {
                document.getElementById("result").innerText += " - You won!";
            }
        }

        // Clear input field
        document.getElementById("wordInput").value = "";
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "An error occurred";
    });
}

function updateHints(guessHistory) {
    const hintList = document.getElementById("hintList");
    hintList.innerHTML = "";  // Clear previous hints

    guessHistory.forEach(entry => {
        const listItem = document.createElement("li");

        // Format the hint nicely
        const formattedHint = entry.hint.map(h => {
            if (h === "_") return "🟡"; // In word, wrong position
            if (h === "X") return "⬛"; // Not in word
            return "🟢"; // Correct position
        }).join("");

        listItem.innerText = `${entry.guess}: ${formattedHint}`;
        hintList.appendChild(listItem);
    });
}

function resetGame() {
    fetch("/reset", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
        document.getElementById("hintList").innerHTML = "";
    })
    .catch(error => console.error("Error:", error));
}

// Add a reset button to your HTML and call this function