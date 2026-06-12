import random
import os

# ─────────────────────────────────────────────
#  Word bank: (word, category, hint)
# ─────────────────────────────────────────────
WORD_BANK = [
    ("PYTHON",         "Programming",      "A popular high-level language named after a snake."),
    ("JAVASCRIPT",     "Programming",      "The scripting language that powers interactive web pages."),
    ("ALGORITHM",      "Computer Science", "A step-by-step procedure for solving a problem."),
    ("VARIABLE",       "Programming",      "A named storage location that holds a value in a program."),
    ("RECURSION",      "Computer Science", "A function that calls itself on a smaller version of the problem."),
    ("DICTIONARY",     "Python",           "A Python data structure that stores key-value pairs."),
    ("EXCEPTION",      "Programming",      "An error that disrupts the normal flow of a program."),
    ("FIBONACCI",      "Mathematics",      "A sequence where each number is the sum of the two before it."),
    ("DATABASE",       "Technology",       "An organised collection of structured data stored electronically."),
    ("COMPILER",       "Computer Science", "Translates source code into machine code."),
    ("INHERITANCE",    "OOP",              "A mechanism where a class acquires properties of another class."),
    ("ENCRYPTION",     "Security",         "Converts data into a secret code to prevent unauthorised access."),
    ("TUPLE",          "Python",           "An immutable ordered sequence written with parentheses."),
    ("ITERATOR",       "Programming",      "An object that lets you traverse elements one at a time."),
    ("FRAMEWORK",      "Technology",       "A pre-built structure that provides tools and conventions for development."),
    ("BINARY",         "Computer Science", "A number system that uses only 0s and 1s."),
    ("HANGMAN",        "Games",            "The word-guessing game you are currently playing!"),
    ("BEAUTIFUL SOUP", "Web Scraping",     "A Python library for parsing HTML and XML documents."),
]

# ─────────────────────────────────────────────
#  Gallows art — index 0 (safe) → 6 (dead)
# ─────────────────────────────────────────────
GALLOWS = [
    # 0 wrong
    """
  +-------+
  |       |
  |
  |
  |
  |
  |
=========""",
    # 1 wrong – head
    """
  +-------+
  |       |
  |       O
  |
  |
  |
  |
=========""",
    # 2 wrong – body
    """
  +-------+
  |       |
  |       O
  |       |
  |       |
  |
  |
=========""",
    # 3 wrong – left arm
    """
  +-------+
  |       |
  |       O
  |      /|
  |       |
  |
  |
=========""",
    # 4 wrong – both arms
    """
  +-------+
  |       |
  |       O
  |      /|\\
  |       |
  |
  |
=========""",
    # 5 wrong – left leg
    """
  +-------+
  |       |
  |       O
  |      /|\\
  |       |
  |      /
  |
=========""",
    # 6 wrong – both legs (dead)
    """
  +-------+
  |       |
  |       O
  |      /|\\
  |       |
  |      / \\
  |
=========""",
]

MAX_WRONG = 6


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def display_word(word: str, guessed: set) -> str:
    """Return the word with un-guessed letters replaced by underscores."""
    return "  ".join(ch if (ch == " " or ch in guessed) else "_" for ch in word)


def progress_bar(word: str, guessed: set, width: int = 20) -> str:
    """Return a text progress bar showing how many letters have been found."""
    letters = [ch for ch in word if ch != " "]
    found   = sum(1 for ch in letters if ch in guessed)
    total   = len(letters)
    filled  = int((found / total) * width)
    bar     = "#" * filled + "-" * (width - filled)
    pct     = int((found / total) * 100)
    return f"  [{bar}]  {found}/{total} letters  ({pct}%)"


def lives_bar(wrong: int) -> str:
    """Return a row of hearts showing remaining lives."""
    remaining = MAX_WRONG - wrong
    return "  " + "♥ " * remaining + "♡ " * wrong + f"  ({remaining} lives left)"


def wrong_letters(guessed: set, word: str) -> str:
    """Return sorted list of incorrect guesses."""
    bad = sorted(ch for ch in guessed if ch not in word)
    return ", ".join(bad) if bad else "none yet"


# ─────────────────────────────────────────────
#  Main game loop
# ─────────────────────────────────────────────
def play():
    word, category, hint = random.choice(WORD_BANK)
    guessed: set  = set()
    wrong:   int  = 0
    hint_used: bool = False

    while True:
        clear()

        # ── Gallows ──
        print(GALLOWS[wrong])

        # ── Status ──
        print(f"  Category : {category}")
        print(lives_bar(wrong))
        print()

        # ── Word display ──
        print("  " + display_word(word, guessed))
        print()

        # ── Progress bar ──
        print("  Progress:")
        print(progress_bar(word, guessed))
        print()

        # ── Wrong guesses ──
        print(f"  Wrong guesses : {wrong_letters(guessed, word)}")
        print()

        # ── Win / Lose check ──
        letters_only = [ch for ch in word if ch != " "]
        won  = all(ch in guessed for ch in letters_only)
        lost = wrong >= MAX_WRONG

        if won:
            print(f"  *** You won! The word was: {word} ***")
            break
        if lost:
            print(f"  *** Game over! The word was: {word} ***")
            break

        # ── Hint option ──
        if not hint_used:
            print("  (Press H for a hint)")

        # ── Input ──
        raw = input("  Guess a letter (or 'H' for hint, 'Q' to quit): ").strip().upper()

        if raw == "Q":
            print(f"\n  You quit. The word was: {word}")
            break

        if raw == "H":
            if hint_used:
                print("  Hint already used!")
            else:
                hint_used = True
                print(f"\n  HINT: {hint}")
                input("  (Press Enter to continue...)")
            continue

        if len(raw) != 1 or not raw.isalpha():
            input("  Please enter a single letter. (Press Enter to continue...)")
            continue

        letter = raw
        if letter in guessed:
            input(f"  You already guessed '{letter}'. (Press Enter to continue...)")
            continue

        guessed.add(letter)

        if letter in word:
            print(f"\n  '{letter}' is in the word!")
        else:
            wrong += 1
            print(f"\n  '{letter}' is NOT in the word.")

        input("  (Press Enter to continue...)")

    # ── Play again? ──
    print()
    again = input("  Play again? (Y/N): ").strip().upper()
    if again == "Y":
        play()
    else:
        print("\n  Thanks for playing Hangman! Goodbye.\n")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n  Welcome to HANGMAN!")
    print("  Guess the word one letter at a time.")
    print("  You have 6 chances before the man is hanged.\n")
    input("  Press Enter to start...")
    play()

