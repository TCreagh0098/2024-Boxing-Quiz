import csv
from functools import partial
from tkinter import *
from tkinter import messagebox
import random


# Function to read boxers from CSV file
def get_all_boxers(file_path):
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            var_all_boxers = [row for row in reader]
            print(f"Successfully read {len(var_all_boxers)} boxers from the CSV file.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        messagebox.showerror("Error", f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        messagebox.showerror("Error", f"Error reading CSV file: {e}")
        return []
    return var_all_boxers


class ChooseWeight:

    def __init__(self, root):
        self.root = root
        self.root.title("Undisputed Quiz")

        # Read all boxers from the CSV file
        self.all_boxers = get_all_boxers("undisputed_boxers_middle.csv")

        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI frame
        self.intro_frame = Frame(self.root, padx=50, pady=60)
        self.intro_frame.grid()

        # Heading and brief instructions
        self.temp_heading = Label(self.intro_frame, text="Undisputed Boxing Champions Quiz",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        choose_instruction_txt = ("\n\nThis quiz will test your boxing"
                                  " knowledge by giving you a date that"
                                  " a boxer became the undisputed "
                                  " champion, you will then be provided "
                                  " with four possible answers in the form "
                                  " of a multi-choice question with one "
                                  " answer being correct...\n\n"
                                  " After completing the quiz you "
                                  " will get a score out of how many "
                                  " questions you got correct e.g. "
                                  " 6/10 or 13/20 etc...\n\n"
                                  " To begin, please choose what "
                                  " weight-class you want to be quizzed on...")

        self.choose_instructions_label = Label(self.intro_frame, text=choose_instruction_txt, wraplength=400,
                                               justify="left")
        self.choose_instructions_label.grid(row=1)

        # Weight class buttons
        self.which_weight_frame = Frame(self.intro_frame)
        self.which_weight_frame.grid(row=2)

        self.heavy_button = Button(self.which_weight_frame, fg=button_fg, bg="#990000", text="Heavyweight",
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("heavyweight"))
        self.heavy_button.grid(row=0, column=0, padx=5, pady=5)

        self.middle_button = Button(self.which_weight_frame, fg=button_fg, bg="#006600", text="Middleweight",
                                    font=button_font, width=13, height=2,
                                    command=lambda: self.weight_select("middleweight"))
        self.middle_button.grid(row=0, column=1, padx=10, pady=10)

        self.light_button = Button(self.which_weight_frame, fg=button_fg, bg="#330066", text="Lightweight",
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("lightweight"))
        self.light_button.grid(row=0, column=2, padx=5, pady=5)

    def weight_select(self, weight_class):
        print(f"Selected weight class: {weight_class}")
        self.intro_frame.destroy()  # Destroy the intro frame before opening the quiz
        self.quiz_window = Toplevel(self.root)
        self.quiz_window.protocol("WM_DELETE_WINDOW", self.on_close_quiz)  # Handle the closing of quiz window
        Quiz(self.quiz_window, weight_class, self.all_boxers)

    def on_close_quiz(self):
        self.quiz_window.destroy()
        self.root.deiconify()


class Quiz:

    def __init__(self, quiz_window, weight_class, all_boxers):
        self.quiz_window = quiz_window
        self.weight_class = weight_class
        self.all_boxers = all_boxers
        self.questions_asked = 0
        self.correct_boxer = ""
        self.score = 0

        self.quiz_window.title("Undisputed Quiz")

        # Frames
        self.intro_frame = Frame(self.quiz_window)
        self.intro_frame.pack(pady=10)

        self.question_frame = Frame(self.quiz_window)
        self.question_frame.pack(pady=10)

        self.answer_frame = Frame(self.quiz_window)
        self.answer_frame.pack(pady=10)

        # Score label
        self.score_label = Label(self.intro_frame, text=f"{self.questions_asked}/20", font=("Helvetica", 16))
        self.score_label.pack()

        # Question label
        self.question_label = Label(self.question_frame, text="", font=("Helvetica", 14), bg="#000000", fg="#FFFFFF",
                                    width=50, height=4)
        self.question_label.pack()

        # Answer buttons
        self.answer_buttons = [
            Button(self.answer_frame, text="", font=("Helvetica", 12), bg="#990000", fg="#FFFFFF", width=20, height=2,
                   command=partial(self.check_answer, i))
            for i in range(4)
        ]

        # Grid layout for answer buttons
        self.answer_buttons[0].grid(row=0, column=0, padx=10, pady=10)
        self.answer_buttons[1].grid(row=0, column=1, padx=10, pady=10)
        self.answer_buttons[2].grid(row=1, column=0, padx=10, pady=10)
        self.answer_buttons[3].grid(row=1, column=1, padx=10, pady=10)

        # Start the first question
        self.update_question()

    def update_question(self):
        print(f"Updating question {self.questions_asked + 1}")
        self.questions_asked += 1

        # Adjust the filtering logic if needed
        weight_class_boxers = [row for row in self.all_boxers if self.weight_class.lower() in row['Boxer'].lower()]
        print(f"Found {len(weight_class_boxers)} boxers for weight class '{self.weight_class}'")

        try:
            boxer_info = random.choice(weight_class_boxers)
            boxer = boxer_info['Boxer']
            reign_start = boxer_info['Reign Start']
            reign_end = boxer_info['Reign End']
            print(f"Selected boxer: {boxer}, Reign Start: {reign_start}, Reign End: {reign_end}")
        except IndexError as e:
            print(f"Error choosing a random boxer: {e}")
            messagebox.showerror("Error", "There was an error selecting a random boxer.")
            self.quiz_window.destroy()
            return

        self.correct_boxer = boxer

        self.question_label.config(text=f"Who became undisputed {self.weight_class} champion in {reign_start}?")

        # Get a list of boxer names, ensuring no repeats
        boxers = set()
        attempts = 0  # Keep track of attempts to prevent infinite loop
        while len(boxers) < 4 and attempts < 100:
            boxer_name = random.choice(weight_class_boxers)['Boxer']
            boxers.add(boxer_name)
            attempts += 1
            print(f"Attempts: {attempts}, Boxers: {boxers}")

        if len(boxers) < 4:
            messagebox.showerror("Error", "Unable to gather enough unique boxers for the quiz.")
            self.quiz_window.destroy()
            return

        boxers = list(boxers)

        print(f"Boxers for question: {boxers}")
        if self.correct_boxer not in boxers:
            boxers[random.randint(0, 3)] = self.correct_boxer

        random.shuffle(boxers)

        for btn, name in zip(self.answer_buttons, boxers):
            btn.config(text=name)

        self.score_label.config(text=f"{self.questions_asked}/20")

    def check_answer(self, index):
        selected_name = self.answer_buttons[index].cget("text")
        if selected_name == self.correct_boxer:
            self.score += 1
            messagebox.showinfo("Correct!", "That's the correct answer!")
        else:
            messagebox.showerror("Wrong!", f"The correct answer was {self.correct_boxer}")

        if self.questions_asked < 20:
            self.update_question()
        else:
            messagebox.showinfo("Quiz Completed", f"You have completed the quiz!\nYour score: {self.score}/20")
            self.quiz_window.destroy()
            self.root.deiconify()  # Show the root window again


# Main routine
if __name__ == "__main__":
    root = Tk()
    ChooseWeight(root)
    root.mainloop()
