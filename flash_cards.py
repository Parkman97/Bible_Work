import tkinter as tk

from get_data import get_random_Verse

# Initialize flashcards globally
flashcards = None

def flash_cards():
    global flashcards  # Declare flashcards as global
    flashcards = get_random_Verse()  # Initialize flashcards
    # Tkinter setup
    root = tk.Tk()
    root.title("Flashcards")

    # Display question
    question_label = tk.Label(root, text=flashcards[0], font=("Helvetica", 18))
    question_label.pack(pady=20)

    # Flip button functionality
    def flip_card():
        global flashcards  # Use the global flashcards
        answer = flashcards[1]
        question_label.config(text=answer)

    def next_card():
        global flashcards  # Use the global flashcards
        flashcards = get_random_Verse()  # Get new random verse
        question_label.config(text=flashcards[0])

    # Buttons for flipping and moving to next card
    flip_button = tk.Button(root, text="Show Answer", command=flip_card)
    flip_button.pack(pady=10)

    next_button = tk.Button(root, text="Next Question", command=next_card)
    next_button.pack(pady=10)

    # Run the application
    root.mainloop()



flash_cards()
