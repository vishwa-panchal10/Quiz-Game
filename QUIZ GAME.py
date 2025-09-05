import tkinter as tk
from tkinter import messagebox, simpledialog

# ----------------- Classes -----------------
class Question:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

class Player:
    def __init__(self):
        self.players = []

    def add_player(self, name):
        self.players.append([name, 0, 0])
        return f"Player '{name}' added!"

    def delete_player(self, index):
        if 0 <= index < len(self.players):
            deleted = self.players.pop(index)
            return f"Player '{deleted[0]}' deleted!"
        return "Invalid index!"

# ----------------- GUI Application -----------------
class QuizApp:
    def __init__(self, root, question_bank):
        self.root = root
        self.root.title("🎮 Quiz Game")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.question_bank = question_bank
        self.players = Player()
        self.current_player = None
        self.question_index = 0
        self.score = 0

        # --- Frames ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20)

        self.menu_frame()
    
    # --- Menu Frame ---
    def menu_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        tk.Label(self.main_frame, text="Quiz Game 🎉", font=("Helvetica", 24, "bold")).pack(pady=20)

        tk.Button(self.main_frame, text="Add Player", width=20, bg="#4CAF50", fg="white", font=("Helvetica", 12),
                  command=self.add_player).pack(pady=5)
        tk.Button(self.main_frame, text="Delete Player", width=20, bg="#f44336", fg="white", font=("Helvetica", 12),
                  command=self.delete_player).pack(pady=5)
        tk.Button(self.main_frame, text="Players Details", width=20, bg="#2196F3", fg="white", font=("Helvetica", 12),
                  command=self.show_players).pack(pady=5)
        tk.Button(self.main_frame, text="Play Quiz", width=20, bg="#FF9800", fg="white", font=("Helvetica", 12),
                  command=self.select_player).pack(pady=5)
        tk.Button(self.main_frame, text="Quit", width=20, bg="#9C27B0", fg="white", font=("Helvetica", 12),
                  command=self.root.quit).pack(pady=5)

    # --- Add Player ---
    def add_player(self):
        name = simpledialog.askstring("Add Player", "Enter player name:")
        if name:
            msg = self.players.add_player(name)
            messagebox.showinfo("Info", msg)

    # --- Delete Player ---
    def delete_player(self):
        if not self.players.players:
            messagebox.showwarning("Warning", "No players to delete!")
            return
        options = "\n".join([f"{i}: {p[0]}" for i, p in enumerate(self.players.players)])
        index = simpledialog.askinteger("Delete Player", f"Select player index:\n{options}")
        msg = self.players.delete_player(index)
        messagebox.showinfo("Info", msg)

    # --- Show Players ---
    def show_players(self):
        if not self.players.players:
            messagebox.showinfo("Players", "No players added yet!")
            return
        details = "\n".join([f"{i}. {p[0]} - Score: {p[1]}, Questions: {p[2]}" for i, p in enumerate(self.players.players)])
        messagebox.showinfo("Players Details", details)

    # --- Select Player ---
    def select_player(self):
        if not self.players.players:
            messagebox.showwarning("Warning", "Please add a player first!")
            return
        options = "\n".join([f"{i}: {p[0]}" for i, p in enumerate(self.players.players)])
        index = simpledialog.askinteger("Select Player", f"Select player index:\n{options}")
        if index is not None and 0 <= index < len(self.players.players):
            self.current_player = index
            self.question_index = 0
            self.score = 0
            self.play_quiz()
        else:
            messagebox.showwarning("Warning", "Invalid selection!")

    # --- Play Quiz ---
    def play_quiz(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.question_index >= len(self.question_bank):
            # Quiz finished
            player = self.players.players[self.current_player]
            player[1] += self.score
            player[2] += len(self.question_bank)
            accuracy = (player[1] / player[2]) * 100
            messagebox.showinfo("Quiz Finished",
                                f"Game Score: {self.score}\nTotal Score: {player[1]}\nAccuracy: {accuracy:.2f}%")
            self.menu_frame()
            return

        q = self.question_bank[self.question_index]
        tk.Label(self.main_frame, text=q.question, font=("Helvetica", 16, "bold"), wraplength=500).pack(pady=20)

        for option in q.options:
            tk.Button(self.main_frame, text=option, font=("Helvetica", 12), width=40,
                      command=lambda ans=option[0]: self.check_answer(ans, q.answer)).pack(pady=5)

    def check_answer(self, selected, correct):
        if selected == correct:
            self.score += 1
        self.question_index += 1
        self.play_quiz()


# ----------------- Question Bank -----------------
question_bank = [
    Question("What is the capital of France?", ["1. Paris", "2. London", "3. Berlin", "4. Madrid"], "1"),
    Question("Which gas do plants absorb from the atmosphere for photosynthesis?",
             ["1. Oxygen", "2. Nitrogen", "3. Carbon Dioxide", "4. Hydrogen"], "3"),
    Question("What is the largest planet in our solar system?", ["1. Earth", "2. Mars", "3. Jupiter", "4. Saturn"], "3"),
    Question("Who wrote 'Romeo and Juliet'?", ["1. William Shakespeare", "2. Charles Dickens", "3. Jane Austen", "4. Leo Tolstoy"], "1"),
    Question("What is the chemical symbol for water?", ["1. H2O", "2. O2", "3. CO2", "4. H2"], "1"),
    Question("In what year did the Titanic sink?", ["1. 1912", "2. 1923", "3. 1905", "4. 1898"], "1"),
    Question("What is the hardest natural substance on Earth?", ["1. Gold", "2. Iron", "3. Diamond", "4. Quartz"], "3"),
    Question("Which planet is known as the Red Planet?", ["1. Mars", "2. Jupiter", "3. Saturn", "4. Venus"], "1"),
    Question("What is the formula for calculating the area of a circle?", ["1. πr^2", "2. 2πr", "3. πr", "4. r^2/π"], "1"),
    Question("Who is known as the father of computer science?", ["1. Albert Einstein", "2. Isaac Newton", "3. Charles Babbage", "4. Alan Turing"], "4")
]

# ----------------- Run App -----------------
root = tk.Tk()
app = QuizApp(root, question_bank)
root.mainloop()
