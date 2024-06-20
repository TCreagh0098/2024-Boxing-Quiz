import csv
import random
from tkinter import *
from tkinter import messagebox
from functools import partial

# Function to read boxers from a specific CSV file
def get_all_boxers(file_name):
    var_all_boxers = []
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)  # Skip header row
        var_all_boxers.extend(list(reader))
    return var_all_boxers

class ChooseWeight:
    def __init__(self, root):
        self.root = root
        self.root.title("Undisputed Quiz")

        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI frame
        self.intro_frame = Frame(self.root, padx=50, pady=60)
        self.intro_frame.grid()

        # Heading and brief instructions
        self.temp_heading = Label(self.intro_frame, text="Undisputed Boxing Champions Quiz",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        choose_instruction_txt = (
            "\n\nThis quiz will test your boxing"
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
            " weight-class you want to be quizzed on..."
        )

        self.choose_instructions_label = Label(self.intro_frame, text=choose_instruction_txt, wraplength=400,
                                               justify="left")
        self.choose_instructions_label.grid(row=1)

        # Weight class buttons
        self.which_weight_frame = Frame(self.intro_frame)
        self.which_weight_frame.grid(row=2)

        self.heavy_button = Button(self.which_weight_frame, fg=button_fg, bg="#990000", text="Heavyweight",
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("heavyweight", "undisputed_boxers_heavy.csv"))
        self.heavy_button.grid(row=0, column=0, padx=5, pady=5)

        self.middle_button = Button(self.which_weight_frame, fg=button_fg, bg="#006600", text="Middleweight",
                                    font=button_font, width=13, height=2,
                                    command=lambda: self.weight_select("middleweight", "undisputed_boxers_middle.csv"))
        self.middle_button.grid(row=0, column=1, padx=10, pady=10)

        self.light_button = Button(self.which_weight_frame, fg=button_fg, bg="#330066", text="Lightweight",
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("lightweight", "undisputed_boxers_light.csv"))
        self.light_button.grid(row=0, column=2, padx=5, pady=5)

    def weight_select(self, weight_class, file_name):
        print(f"Selected weight class: {weight_class}")
        self.intro_frame.destroy()  # Destroy the intro frame before opening the quiz
        self.quiz_window = Toplevel(self.root)
        self.quiz_window.protocol("WM_DELETE_WINDOW", self.on_close_quiz)  # Handle the closing of quiz window
        all_boxers = get_all_boxers(file_name)
        Quiz(self.quiz_window, weight_class, all_boxers)

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

    def get_round_boxers(self, weight_class_boxers):
        round_boxers_list = []
        while len(round_boxers_list) < 4:
            chosen_boxer = random.choice(weight_class_boxers)
            if chosen_boxer not in round_boxers_list:
                round_boxers_list.append(chosen_boxer)
        return round_boxers_list

    def update_question(self):
        print(f"Updating question {self.questions_asked + 1}")
        self.questions_asked += 1

        weight_class_boxers = self.all_boxers
        print(f"Found {len(weight_class_boxers)} boxers for weight class '{self.weight_class}'")

        if not weight_class_boxers:
            messagebox.showerror("Error", f"No boxers found for weight class '{self.weight_class}'.")
            self.quiz_window.destroy()
            return

        try:
            boxer_info = random.choice(weight_class_boxers)
            boxer = boxer_info[0]
            reign_start = boxer_info[1]
            reign_end = boxer_info[2]
            print(f"Selected boxer: {boxer}, Reign Start: {reign_start}, Reign End: {reign_end}")
        except IndexError as e:
            print(f"Error choosing a random boxer: {e}")
            messagebox.showerror("Error", "There was an error selecting a random boxer.")
            self.quiz_window.destroy()
            return

        self.correct_boxer = boxer

        self.question_label.config(text=f"Who became undisputed {self.weight_class} champion in {reign_start}?")

        # Get four unique boxers for the answer buttons
        round_boxers = self.get_round_boxers(weight_class_boxers)
        if self.correct_boxer not in [boxer[0] for boxer in round_boxers]:
            round_boxers[random.randint(0, 3)][0] = self.correct_boxer

        random.shuffle(round_boxers)

        for btn, boxer_info in zip(self.answer_buttons, round_boxers):
            btn.config(text=boxer_info[0])

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
