import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from PIL import Image, ImageTk
import time
import csv


class HangmanGame:

    def save_user_info(self, username, age_group, subject, score=None, feedback=None):
        file_exists = False
        try:
            with open("users.csv", "r") as file:
                file_exists = True  # File already exists
        except FileNotFoundError:
            pass  # File does not exist, will be created

        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            # Write the header only if the file is newly created
            if not file_exists:
                writer.writerow(["Username", "Age Group", "Subject", "Score", "Feedback"])
            # Append new user data with optional score and feedback
            writer.writerow([username, age_group, subject, score if score is not None else "", feedback if feedback is not None else ""])

    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("500x700")
        self.root.configure(bg="#f0f8ff")  # Light blue background
        self.logo_image = self.overlay_logos()  # Load merged logo
        self.logo_label = tk.Label(self.root, image=self.logo_image, bg="#f0f8ff")
        self.logo_label.pack(pady=10)  # Display logo on all pages

        self.username = None
        self.age_group = None
        self.subject = None
        self.questions = []
        self.current_question_index = 0
        self.word = ""
        self.clue = ""
        self.guessed_word = []
        self.attempts = 6
        self.wrong_guesses = []
        self.score = 0

        self.subjects_by_age = {
            "6-10": ["English", "Maths", "GK"],
            "11-15": ["English", "Maths", "Physics", "Chemistry", "Biology", "Social", "GK"],
            "16-20": ["Physics", "Chemistry", "Biology", "Computer Science", "Economics", "Commerce", "Business Maths"],
            "21-25": ["Physics", "Chemistry", "Biology", "Computer Science", "Accounts", "Economics", "Business Maths", "Commerce"]
        }

        self.word_list = {
            "English": {
                "apple": "A fruit", "book": "For reading", "pencil": "For writing", "chair": "Used for sitting",
                "school": "A place for learning", "teacher": "Educator", "river": "Flowing water",
                "mountain": "High landform", "animal": "Living being", "computer": "A machine"
            },
            "Maths": {
                "circle": "Round shape", "square": "4 equal sides", "addition": "Adding numbers",
                "subtraction": "Opposite of addition", "multiplication": "Repeated addition",
                "division": "Splitting into parts", "algebra": "Math with symbols", "geometry": "Study of shapes",
                "percentage": "Fraction of 100", "fraction": "Part of a whole"
            },
            "GK": {
                "earth": "Our planet", "sun": "Star at center of solar system", "ocean": "Large water body",
                "president": "Head of a country", "volcano": "Erupting mountain", "oxygen": "Gas we breathe",
                "gravity": "Force pulling objects down", "rainbow": "7 colors in the sky", "moon": "Earth's satellite",
                "telescope": "Device to see far"
            },
            "Physics": {
                "force": "Push or pull", "motion": "Movement", "gravity": "Attraction between objects",
                "energy": "Capacity to do work", "friction": "Opposes motion", "inertia": "Resistance to change",
                "acceleration": "Rate of velocity change", "thermodynamics": "Heat and energy study",
                "wave": "Oscillation", "electricity": "Flow of charge"
            },
            "Chemistry": {
                "atom": "Basic unit of matter", "molecule": "Group of atoms", "reaction": "Chemical change",
                "acid": "pH less than 7", "base": "pH more than 7", "salt": "Neutral compound",
                "catalyst": "Speeds up reaction", "solution": "Mixture of substances", "element": "Pure substance",
                "compound": "Two or more elements combined"
            },
            "Biology": {
                "cell": "Basic unit of life", "tissue": "Group of cells", "organ": "Group of tissues",
                "organism": "Living being", "photosynthesis": "Plants making food", "respiration": "Breathing process",
                "gene": "Carries DNA", "virus": "Non-living infectious agent", "bacteria": "Single-celled organism",
                "fungus": "Mold and mushrooms"
            },
            "Computer Science": {
                "binary": "0s and 1s", "algorithm": "Set of instructions", "programming": "Coding process",
                "software": "Set of programs", "hardware": "Physical computer parts", "database": "Collection of data",
                "network": "Connected computers", "cybersecurity": "Protection of data", "AI": "Artificial intelligence",
                "cloud": "Online storage"
            },
            "Economics": {
                "demand": "Consumer need", "supply": "Goods available", "market": "Buying and selling place",
                "inflation": "Rising prices", "GDP": "Total production value", "recession": "Economic slowdown",
                "budget": "Financial plan", "tax": "Government charge", "trade": "Exchange of goods",
                "capital": "Financial assets"
            },
            "Commerce": {
                "business": "Buying and selling", "profit": "Financial gain", "loss": "Negative revenue",
                "investment": "Money put into business", "trade": "Exchange of goods", "market": "Selling place",
                "stock": "Company shares", "entrepreneur": "Business owner", "finance": "Managing money",
                "taxation": "Government revenue system"
            },
            "Social": {
                "kingdom": "Ruled by a king or queen",
                "democracy": "Government by the people",
                "parliament": "Place where laws are made",
                "globe": "Model of Earth",
                "constitution": "Supreme law of a country",
                "monument": "Structure built to honor someone/something",
                "trade": "Exchange of goods and services",
                "climate": "Average weather condition of a place",
                "revolution": "Sudden change in government",
                "citizen": "Member of a country"
            },
            "Business Maths": {
                "profit": "Money gained in business",
                "loss": "Opposite of profit",
                "interest": "Extra money paid on a loan",
                "discount": "Reduction in price",
                "percentage": "Fraction of 100",
                "tax": "Money paid to the government",
                "investment": "Money put into a business for growth",
                "ratio": "Comparison of two numbers",
                "equation": "A mathematical statement with an equals sign",
                "revenue": "Total money earned"
            },
            "Accounts": {
                "ledger": "Book for recording financial transactions",
                "balance": "Difference between total credits and debits",
                "assets": "Things a business owns",
                "liabilities": "Money a company owes",
                "capital": "Money invested in a business",
                "audit": "Checking financial records",
                "depreciation": "Decrease in asset value over time",
                "invoice": "Bill for goods or services",
                "credit": "Money received or borrowed",
                "debit": "Money spent or owed"
            }
        }
        self.ask_username()

    def clear_window(self):
        """Clears all widgets from the window except the logo."""
        for widget in self.root.winfo_children():
            if widget != self.logo_label:  # Don't remove the logo
                widget.destroy()

    def overlay_logos(self):
        """Overlay a second logo on top of the first logo."""
        try:
            background = Image.open("logo (1).png")  # Main logo
            overlay = Image.open("tcarts (1).png")  # Second logo

            # Resize the overlay to be smaller and centered
            overlay = overlay.resize((70, 70))  # Adjust size as needed
            bg_width, bg_height = background.size
            overlay_x = (bg_width - overlay.width) // 2
            overlay_y = (bg_height - overlay.height) // 2

            # Paste overlay on background
            background.paste(overlay, (overlay_x, overlay_y), overlay if overlay.mode == "RGBA" else None)

            # Convert for Tkinter display
            return ImageTk.PhotoImage(background)

        except Exception as e:
            print("Error loading logos:", e)
            return None

    def ask_username(self):
        """Ask for the player's name and validate input."""
        self.clear_window()

        tk.Label(self.root, text="Welcome to the Hangman Game!",
                 font=('Arial', 16, 'bold'), bg="#f0f8ff", fg="dark blue").pack(pady=5)

        tk.Label(self.root, text="Created by: ANISHA N , BHUVANESHWARI M , GANGA LAKSHMI J",
                 font=('Arial', 12, 'bold'), bg="#f0f8ff", fg="black").pack(pady=5)

        tk.Label(self.root, text="Enter Your Name:", font=('Arial', 14), bg="#f0f8ff").pack(pady=10)
        self.name_entry = tk.Entry(self.root, font=('Arial', 14))
        self.name_entry.pack(pady=5)

        tk.Button(self.root, text="Next", font=('Arial', 14), command=self.get_username, bg="#87CEEB").pack(pady=10)

    def get_username(self):
        """Get the username and proceed to age selection."""
        username = self.name_entry.get().strip()

        # Validate username (only letters allowed)
        if not username.isalpha():
            messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
            return

        self.username = username  # Store username properly
        self.choose_age_group()  # Proceed to next step

    def choose_age_group(self, username=None):
        """Ask for age group selection with back button handling."""
        if username:
            self.username = username  # Preserve username when coming back

        self.clear_window()

        tk.Label(self.root, text=f"Hello {self.username}! Choose Your Age Group:", font=('Arial', 14), bg="#f0f8ff").pack(pady=10)

        for age in self.subjects_by_age.keys():
            tk.Button(self.root, text=age, font=('Arial', 14), command=lambda a=age: self.choose_subject(a), bg="#87CEEB").pack(pady=5)

        # Add Back Button
        tk.Button(self.root, text="Back", font=('Arial', 14), command=self.ask_username, bg="red", fg="white").pack(pady=10)

    def choose_subject(self, age_group):
        """Ask for subject selection with back button to age selection."""
        self.age_group = age_group
        self.clear_window()

        tk.Label(self.root, text=f"Choose Your Subject ({self.age_group}):", font=('Arial', 14), bg="#f0f8ff").pack(pady=10)

        for subject in self.subjects_by_age[age_group]:
            tk.Button(self.root, text=subject, font=('Arial', 14), command=lambda s=subject: self.confirm_selection(s), bg="#87CEEB").pack(pady=5)

        # Back Button - Ensures `choose_age_group()` knows the username
        tk.Button(self.root, text="Back", font=('Arial', 14), command=lambda: self.choose_age_group(self.username), bg="red", fg="white").pack(pady=10)

    def start_game(self, subject):
        """Start the Hangman game with 10 words from the chosen subject."""
        self.subject = subject
        words = list(self.word_list.get(subject, {}).keys())

        if len(words) == 0:
            messagebox.showerror("Error", "No words found for this subject!")
            return

        self.questions = words if len(words) < 10 else random.sample(words, 10)
        self.current_question_index = 0
        self.score = 0  # Reset score at the start of a new subject
        self.next_question()

    def show_final_score(self):
     self.clear_window()

     tk.Label(self.root, text=f"Game Over, {self.username}!", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

     # Create a score label
     self.score_label = tk.Label(self.root, text="Score: 0/10", font=("Arial", 24, "bold"), bg="#f0f8ff", fg="black")
     self.score_label.pack(pady=20)

     # Start the animated score update
     self.animate_score(0)

    def animate_score(self, current):
     # Check if the current score is less than the final score
     if current <= self.score:
        self.score_label.config(text=f"Score: {current}/10")
        # Schedule next update after 200ms
        self.root.after(200, lambda: self.animate_score(current + 1))
     else:
        # After the animation, display a message and buttons
        if self.score == 10:
            message = "🏆 Perfect Score! You're a Hangman Champion!"
            color = "gold"
        elif self.score >= 7:
            message = "🎉 Great Job! You did really well!"
            color = "green"
        elif self.score >= 4:
            message = "🙂 Good Try! Keep practicing!"
            color = "blue"
        else:
            message = "😢 Better luck next time! Try again!"
            color = "red"

        tk.Label(self.root, text=message, font=("Arial", 16, "bold"), fg=color, bg="#f0f8ff").pack(pady=20)

        # Delay transition to feedback page (e.g., 2000ms after animation completes)
        self.root.after(2000, lambda: self.get_feedback(self.username, self.age_group, self.subject, self.score))


    def next_question(self):
        """Move to the next question or finish the game."""
        if self.current_question_index >= len(self.questions):
            self.show_final_score()
            return

        self.word = self.questions[self.current_question_index]
        self.clue = self.word_list[self.subject][self.word]
        self.guessed_word = ["_"] * len(self.word)
        self.attempts = 6
        self.wrong_guesses = []
        self.current_question_index += 1

        self.create_widgets()

    def create_widgets(self):
        """Create game UI elements."""
        self.clear_window()

        tk.Label(self.root, text=f"Player: {self.username}  |  Age Group: {self.age_group}  |  Subject: {self.subject}",
                 font=('Arial', 12), bg="#f0f8ff").pack(pady=5)

        tk.Label(self.root, text=f"Question {self.current_question_index}/10", font=('Arial', 14), bg="#f0f8ff").pack(pady=5)
        tk.Label(self.root, text="CLUE: " + self.clue, font=('Comic Sans MS', 14), bg="#f0f8ff").pack(pady=5)

        self.display_word_label = tk.Label(self.root, text=" ".join(self.guessed_word), font=('Arial', 20), bg="#f0f8ff")
        self.display_word_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.root, font=('Arial', 14))
        self.guess_entry.pack(pady=5)
        self.guess_entry.focus()

        # Bind Enter key to check_guess function
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        tk.Button(self.root, text="GUESS", font=('Arial', 14), command=self.check_guess, bg="#87CEEB").pack(pady=5)

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts}", font=('Arial', 12), bg="#f0f8ff")
        self.attempts_label.pack(pady=5)

        self.wrong_guesses_label = tk.Label(self.root, text="Wrong guesses: ", font=('Arial', 12), bg="#f0f8ff")
        self.wrong_guesses_label.pack(pady=5)

        # Canvas for drawing the hangman
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#f0f8ff")
        self.canvas.pack(pady=20)

    def check_guess(self):
        """Check if guessed letter is correct and move to next question automatically."""
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.wrong_guesses or guess in self.guessed_word:
            messagebox.showinfo("Already Guessed", f"{self.username}, you already guessed '{guess}'!")
            return

        if guess in self.word:
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    self.guessed_word[i] = guess
            self.display_word_label.config(text=" ".join(self.guessed_word))

            # If the word is completely guessed, move to the next question after 1 second
            if "_" not in self.guessed_word:
                self.score += 1  # Increase score for correct word
                self.root.after(1000, self.next_question)
        else:
            self.wrong_guesses.append(guess)
            self.wrong_guesses_label.config(text=f"Wrong guesses: {', '.join(self.wrong_guesses)}")
            self.attempts -= 1
            self.attempts_label.config(text=f"Attempts left: {self.attempts}")
            self.draw_hangman()

            if self.attempts == 0:
                # Show correct answer in red and move to next question after 2 seconds
                self.display_word_label.config(text=self.word, fg="red")
                self.root.after(2000, self.next_question)

    def draw_hangman(self):
        """Draw the hangman step by step as attempts decrease."""
        if self.attempts == 5:
            self.canvas.create_line(50, 150, 150, 150, width=5)  # Base
        elif self.attempts == 4:
            self.canvas.create_line(100, 150, 100, 50, width=5)  # Pole
        elif self.attempts == 3:
            self.canvas.create_line(100, 50, 150, 50, width=5)  # Top bar
        elif self.attempts == 2:
            self.canvas.create_line(150, 50, 150, 75, width=5)  # Rope
        elif self.attempts == 1:
            self.canvas.create_oval(140, 75, 160, 95, width=5)  # Head
        elif self.attempts == 0:
            self.canvas.create_line(150, 95, 150, 120, width=5)  # Body
            self.canvas.create_line(150, 110, 130, 130, width=5)  # Left leg
            self.canvas.create_line(150, 110, 170, 130, width=5)  # Right leg
            self.canvas.create_line(150, 85, 130, 100, width=5)  # Left arm
            self.canvas.create_line(150, 85, 170, 100, width=5)  # Right arm

    def confirm_selection(self, subject):
        """Confirm subject selection and start the game."""
        self.subject = subject
        confirmation = messagebox.askyesno("Confirm", f"Do you want to play {self.subject}?")
        if confirmation:
            self.start_game(self.subject)  # Start the game if confirmed
        else:
            self.choose_subject(self.age_group)  # Go back to subject selection

    def get_feedback(self, username, age_group, subject, score):
        """Ask for feedback after the game and save user data."""
        self.clear_window()

        tk.Label(self.root, text=f"Thanks for playing, {username}!", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.root, text="Please share your feedback:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)

        self.feedback_entry = tk.Entry(self.root, font=("Arial", 14), width=40)
        self.feedback_entry.pack(pady=5)

        tk.Button(self.root, text="Submit", font=("Arial", 14), bg="#87CEEB", command=lambda: self.save_feedback(username, age_group, subject, score)).pack(pady=10)

    def save_feedback(self, username, age_group, subject, score):
        """Save user feedback and display a thank you message."""
        feedback = self.feedback_entry.get().strip()
        self.save_user_info(username, age_group, subject, score, feedback)  # Save to CSV
        messagebox.showinfo("Thank You!", "Thank you for playing!")
        self.ask_username()  # Restart the game


root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
