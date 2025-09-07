🍌 Bananagram Game (Tkinter + Python)
====================================

This is a Bananagram-inspired word-building game built with Python’s `tkinter` GUI toolkit.  
Players drag and place letters on a grid to form valid English words, racing against the clock to maximize their score.  

------------------------------------
✨ Features
------------------------------------
- Interactive Grid Board: Place letters on a 25×25 grid using drag & click.
- Randomized Letter Distribution: Tiles are randomly drawn from a shuffled pool.
- Countdown Timer (2 minutes): The game runs against a timer with automatic game-over.
- Word Validation: Uses the NLTK `words` corpus to validate English words.
- Game Actions:
  * More Character → Draws additional tiles (limited to 4 times).
  * Peel → Draws a new tile if the rack is empty.
  * Dump → Exchanges one letter for three new tiles.
  * Banana → Submits your board and checks for valid words.
  * Reset → Resets the entire game.
- Scoring System: Each valid word adds points equal to the number of letters in it.  
  Successfully matched words are highlighted on the grid.

------------------------------------
🖥️ Requirements
------------------------------------
- Python 3.7+
- Tkinter (usually comes pre-installed with Python)
- NLTK (pip install nltk)

First time running? Download the NLTK words corpus:

    import nltk
    nltk.download('words')

------------------------------------
▶️ How to Run
------------------------------------
1. Clone or download the script.
2. Install dependencies:

       pip install nltk

3. Run the game:

       python bananagram.py

------------------------------------
🎮 Controls
------------------------------------
- Left Click (rack) → Select a letter from the rack.
- Left Click (board) → Place the selected letter on the grid.
- Right Click (board) → Withdraw a placed letter back to the rack.

------------------------------------
📊 Game Flow
------------------------------------
1. Start with a set of random letters in your rack.
2. Place them on the grid to form words.
3. Use Peel, Dump, More Character actions strategically.
4. Submit with Banana to check for valid words.
5. Try to score as high as possible before the timer runs out!

------------------------------------
⚠️ Notes
------------------------------------
- Word matching only works with valid NLTK dictionary words.
- Maximum 144 letters can be placed on the board.
- More Character button is limited to 4 uses.
- The game ends when you press Banana or the timer reaches 00:00.

------------------------------------
📌 Future Improvements
------------------------------------
- Multiplayer support
- Custom dictionary or difficulty levels
- Leaderboard / High score saving
- Animations for placed/matched words
