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
        self.intro_frame.destroy()
        NumberQuestions(self.root, weight_class, file_name)


class NumberQuestions:
    def __init__(self, root, weight_class, file_name):
        self.root = root
        self.weight_class = weight_class
        self.file_name = file_name

        # initialise variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")
        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # set up GUI frame
        self.question_frame = Frame(self.root, padx=50, pady=60)
        self.question_frame.grid()

        self.question_heading = Label(self.question_frame,
                                      text="Undisputed Quiz",
                                      font=("Arial", "16", "bold")
                                      )
        self.question_heading.grid(row=0)

        instructions = "To continue with the quiz please enter " \
                       "how many questions you wish to " \
                       "answer...\n\nDepending on which weight " \
                       " class you selected there will be a limit " \
                       "to how many questions can be " \
                       "generated...\n\nHow many questions do " \
                       "you want to be generated..."
        self.question_instructions = Label(self.question_frame,
                                           text=instructions,
                                           wrap=250, width=40,
                                           justify="left")
        self.question_instructions.grid(row=1)

        self.question_entry = Entry(self.question_frame,
                                    font=("Arial", "14")
                                    )
        self.question_entry.grid(row=2, padx=10, pady=10)

        self.output_label = Label(self.question_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        # conversion, help and history / export buttons
        self.button_frame = Frame(self.question_frame)
        self.button_frame.grid(row=4)

        self.quiz_begin_button = Button(self.button_frame,
                                        text="Begin",
                                        bg="#006600",
                                        fg="#FFFFFF",
                                        font=("Arial", "12", "bold"), width=12,
                                        command=self.start_quiz)
        self.quiz_begin_button.grid(row=0, column=0, padx=5, pady=5)

    def check_question(self, min_value, max_value):
        has_error = "no"
        response = self.question_entry.get()

        try:
            response = float(response)
            if not (min_value <= response <= max_value):
                has_error = "yes"
        except ValueError:
            has_error = "yes"

        if has_error == "yes":
            error = f"Please enter a number greater than {min_value} and less than {max_value}"
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"
        else:
            self.var_has_error.set("no")
            return int(response)

    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            self.output_label.config(fg="#9C0000")
            self.question_entry.config(bg="#F8CECC")
        else:
            self.output_label.config(fg="#004C00")
            self.question_entry.config(bg="#CCFFCC")

        self.output_label.config(text=output)

    def start_quiz(self):
        min_value = 1
        max_value = 20  # assuming a maximum of 20 questions
        result = self.check_question(min_value, max_value)
        self.output_answer()
        if result != "invalid":
            self.question_frame.destroy()
            all_boxers = get_all_boxers(self.file_name)
            Quiz(self.root, self.weight_class, all_boxers, result)


class Quiz:
    def __init__(self, root, weight_class, all_boxers, num_questions):
        self.root = root
        self.weight_class = weight_class
        self.all_boxers = all_boxers
        self.num_questions = num_questions
        self.questions_asked = 0
        self.correct_boxer = ""
        self.score = 0

        self.root.title("Undisputed Quiz")

        # Frames
        self.intro_frame = Frame(self.root)
        self.intro_frame.pack(pady=10)

        self.question_frame = Frame(self.root)
        self.question_frame.pack(pady=10)

        self.answer_frame = Frame(self.root)
        self.answer_frame.pack(pady=10)

        # Score label
        self.score_label = Label(self.intro_frame, text="{}/{}".format(self.questions_asked, self.num_questions),
                                 font=("Helvetica", 16))
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
        self.questions_asked += 1

        weight_class_boxers = self.all_boxers

        if not weight_class_boxers:
            messagebox.showerror("Error", f"No boxers found for weight class '{self.weight_class}'.")
            self.root.destroy()
            return

        try:
            boxer_info = random.choice(weight_class_boxers)
            boxer = boxer_info[0]
            reign_start = boxer_info[1]
            reign_end = boxer_info[2]
        except IndexError as e:
            messagebox.showerror("Error", "There was an error selecting a random boxer.")
            self.root.destroy()
            return

        self.correct_boxer = boxer
        self.question_label.config(text=f"Who became undisputed {self.weight_class} champion in {reign_start}?")

        round_boxers = self.get_round_boxers(weight_class_boxers)
        if self.correct_boxer not in [boxer[0] for boxer in round_boxers]:
            round_boxers[random.randint(0, 3)][0] = self.correct_boxer

        random.shuffle(round_boxers)

        for btn, boxer_info in zip(self.answer_buttons, round_boxers):
            btn.config(text=boxer_info[0])

        self.score_label.config(text=f"{self.questions_asked}/{self.num_questions}")

    def check_answer(self, index):
        selected_name = self.answer_buttons[index].cget("text")
        if selected_name == self.correct_boxer:
            self.score += 1
            messagebox.showinfo("Correct!", "That's the correct answer!")
        else:
            messagebox.showerror("Wrong!", f"The correct answer was {self.correct_boxer}")

        if self.questions_asked < self.num_questions:
            self.update_question()
        else:
            global user_score, questions_answered
            user_score = self.score
            questions_answered = self.num_questions
            self.show_end_screen()

    def show_end_screen(self):
        self.intro_frame.destroy()
        self.question_frame.destroy()
        self.answer_frame.destroy()
        EndScreen(self.root)


class EndScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Undisputed Quiz")

        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        self.frame = Frame(self.root, padx=50, pady=50)
        self.frame.pack()

        self.intro_frame = Frame(self.frame, pady=10)
        self.intro_frame.grid(row=0, columnspan=3)

        self.congrats_label = Label(self.intro_frame, text="Congratulations!", font=("Arial", 24), fg="#006600")
        self.congrats_label.pack()

        self.score_label = Label(self.intro_frame, text="You got *{}* / *{}*".format(user_score, questions_answered),
                                 font=("Arial", 14), fg="#006600")
        self.score_label.pack()

        self.winner_frame = Frame(self.frame, pady=10)
        self.winner_frame.grid(row=1, columnspan=3)

        self.winner_image = PhotoImage(file="Winner_Belt.png")  # Adjust path as necessary
        self.winner_label = Label(self.winner_frame, image=self.winner_image)
        self.winner_label.pack()

        # Keep a reference to the image to prevent garbage collection
        self.winner_label.image = self.winner_image

        self.buttons_frame = Frame(self.frame, pady=10)
        self.buttons_frame.grid(row=2, columnspan=3)

        self.stats_button = Button(self.buttons_frame, text="Stats", bg="#330066", fg="#FFFFFF", font=button_font,
                                   width=13, height=2)
        self.stats_button.grid(row=0, column=0, padx=10)

        self.play_again_button = Button(self.buttons_frame, text="Play Again", bg="#006600", fg="#FFFFFF",
                                        font=button_font, width=13, height=2, command=self.play_again)
        self.play_again_button.grid(row=0, column=1, padx=10)

        self.exit_button = Button(self.buttons_frame, text="Exit", bg="#990000", fg="#FFFFFF", font=button_font,
                                  width=13, height=2, command=self.root.quit)
        self.exit_button.grid(row=0, column=2, padx=10)

    def play_again(self):
        self.frame.destroy()
        ChooseWeight(self.root)


# Main routine
if __name__ == "__main__":
    user_score = 0
    questions_answered = 0

    root = Tk()
    ChooseWeight(root)
    root.mainloop()
