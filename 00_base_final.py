import csv
import random
from tkinter import *
from tkinter import messagebox
from functools import partial

# List to store attempts data across multiple quiz rounds
attempts_data = []

# Function to read boxer data from a CSV file
def get_all_boxers(file_name):
    var_all_boxers = []
    with open(file_name, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)  # Skip the header row in the CSV file
        var_all_boxers.extend(list(reader))  # Add all rows from the CSV to the list
    return var_all_boxers


# Function to calculate and return statistics based on past quiz attempts
def stats(attempts):
    recent_attempts = attempts[-3:]  # Get the last 3 attempts
    total_questions = sum(attempt["questions_asked"] for attempt in attempts)
    total_correct_answers = sum(attempt["correct_answers"] for attempt in attempts)

    if total_questions > 0:
        # Calculate the average percentage of correct answers
        average_correct_percentage = round((total_correct_answers / total_questions) * 100)
    else:
        average_correct_percentage = 0

    return {
        "recent_attempts": recent_attempts,
        "average_correct_percentage": average_correct_percentage,
        "total_correct_answers": total_correct_answers,
        "total_questions_asked": total_questions
    }


# Class to display statistics in a new window
class DisplayStats:
    def __init__(self, partner, attempts):
        self.stats_box = Toplevel()  # Create a new window for statistics

        stats_bg_colour = "#FFFFFF"
        partner.stats_button.config(state=DISABLED)  # Disable the stats button on the main window
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))  # Handle window close event

        self.stats_frame = Frame(self.stats_box, width=400, height=250, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame, text="Statistics", font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=0)

        # Information text displayed in the statistics window
        stats_text = "Here are your quiz statistics...\n\nYour last 3 attempts will be " \
                     "displayed here along with your combined average percentage and total " \
                     "answers for all previous attempts..."
        self.help_text_label = Label(self.stats_frame, text=stats_text, wraplength=350, justify="left",
                                     bg=stats_bg_colour)
        self.help_text_label.grid(row=1, padx=10, pady=10)

        # Frame to contain statistics data
        self.data_frame = Frame(self.stats_frame, bg="#FFFFFF", borderwidth=1, relief="solid", height="80")
        self.data_frame.grid(row=2, column=0, padx=2, pady=2)

        # Retrieve stats based on attempts
        stats_output = stats(attempts)
        recent_attempts = stats_output["recent_attempts"]
        average_correct_percentage = stats_output["average_correct_percentage"]
        total_correct_answers = stats_output["total_correct_answers"]
        total_questions_asked = stats_output["total_questions_asked"]

        head_back = "#990000"  # Background color for header
        text_color = "#FFFFFF"  # Text color for labels

        # Display recent attempts as "correct answers / questions asked"
        row = 0
        for attempt in recent_attempts:
            attempt_text = "{} / {}".format(attempt['correct_answers'], attempt['questions_asked'])
            self.attempts_data_label = Label(self.data_frame, text=attempt_text, bg=head_back, width=20, height=2,
                                             padx=5, borderwidth=1, relief="solid", fg=text_color)
            self.attempts_data_label.grid(row=row, column=0, padx=2, pady=2)
            row += 1

        # Displays total statistics such as total questions asked, correct answers, and average percentage
        stats_labels = [
            "Total Questions Asked: {}".format(total_questions_asked),
            "Total Correct Answers: {}".format(total_correct_answers),
            "Average Correct Percentage: {}%".format(average_correct_percentage)
        ]

        row = 0
        for label_text in stats_labels:
            self.label = Label(self.data_frame, text=label_text, bg=head_back, width=30, height=2,
                               padx=5, borderwidth=1, relief="solid", fg=text_color)
            self.label.grid(row=row, column=1, padx=2, pady=2)
            row += 1

    # Function to close the statistics window and re-enable the stats button in the main window
    def close_stats(self, partner):
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# Class to allow the user to choose the weight class for the quiz
class ChooseWeight:
    def __init__(self, root):
        self.root = root
        self.root.title("Undisputed Quiz")

        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # Set up the introductory GUI frame
        self.intro_frame = Frame(self.root, padx=50, pady=60)
        self.intro_frame.grid()

        # Heading label and instructions
        self.temp_heading = Label(self.intro_frame, text="Undisputed Boxing Champions Quiz",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        # Instructions for choosing the weight class
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

        # Frame for weight class buttons
        self.which_weight_frame = Frame(self.intro_frame)
        self.which_weight_frame.grid(row=2)

        # Buttons for selecting weight classes
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

    # Function to handle the selection of a weight class
    def weight_select(self, weight_class, file_name):
        self.intro_frame.destroy()  # Destroy the intro frame
        NumberQuestions(self.root, weight_class, file_name)  # Proceed to the number of questions screen


# Class to allow the user to specify the number of questions for the quiz
class NumberQuestions:
    def __init__(self, root, weight_class, file_name):
        self.root = root
        self.weight_class = weight_class
        self.file_name = file_name

        # Initialize feedback variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")
        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # Set up the GUI frame
        self.question_frame = Frame(self.root, padx=50, pady=60)
        self.question_frame.grid()

        # Heading label
        self.question_heading = Label(self.question_frame,
                                      text="Undisputed Quiz",
                                      font=("Arial", "16", "bold")
                                      )
        self.question_heading.grid(row=0)

        # Instructions for entering the number of questions
        instructions = "To continue with the quiz please enter " \
                       "how many questions you wish to " \
                       "answer...\n\nYou must enter a whole number with 20 " \
                       "questions being the maximum amount" \
                       "...\n\nHow many questions do " \
                       "you want to be generated..."
        self.question_instructions = Label(self.question_frame,
                                           text=instructions,
                                           wrap=250, width=40,
                                           justify="left")
        self.question_instructions.grid(row=1)

        # Entry field for the number of questions
        self.question_entry = Entry(self.question_frame,
                                    font=("Arial", "14")
                                    )
        self.question_entry.grid(row=2, padx=10, pady=10)

        self.output_label = Label(self.question_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        # Frame for the buttons
        self.button_frame = Frame(self.question_frame)
        self.button_frame.grid(row=4)

        # Button to start the quiz
        self.quiz_begin_button = Button(self.button_frame,
                                        text="Begin",
                                        bg="#006600",
                                        fg="#FFFFFF",
                                        font=("Arial", "12", "bold"), width=12,
                                        command=self.start_quiz)
        self.quiz_begin_button.grid(row=0, column=0, padx=5, pady=5)

    # Function to check if the entered number of questions is valid
    def check_question(self, min_value, max_value):
        has_error = "no"
        response = self.question_entry.get()  # Get user input

        try:
            response = int(response)  # Try converting input to an integer
            if not (min_value <= response <= max_value):  # Check if input is within the valid range
                has_error = "yes"
        except ValueError:
            has_error = "yes"  # Input is not a valid integer

        if has_error == "yes":
            error = f"Please enter a whole number ≥ to {min_value} or ≤ to {max_value}"
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"
        else:
            self.var_has_error.set("no")
            return int(response)

    # Function to output the result of the input validation
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

    # Function to start the quiz after validating the number of questions
    def start_quiz(self):
        min_value = 1
        max_value = 20  # Maximum number of questions is 20
        result = self.check_question(min_value, max_value)
        self.output_answer()
        if result != "invalid":
            self.question_frame.destroy()  # Destroy the current frame
            all_boxers = get_all_boxers(self.file_name)  # Get the list of boxers from the CSV file
            Quiz(self.root, self.weight_class, all_boxers, result)  # Start the quiz


# Class to handle the quiz logic and display
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

        # Define color map for different weight classes
        self.color_map = {
            "heavyweight": "#990000",
            "middleweight": "#006600",
            "lightweight": "#330066"
        }

        # Set up frames for different sections of the quiz
        self.intro_frame = Frame(self.root)
        self.intro_frame.pack(pady=10)

        self.question_frame = Frame(self.root)
        self.question_frame.pack(pady=10)

        self.answer_frame = Frame(self.root)
        self.answer_frame.pack(pady=10)

        # Label to display the current score
        self.score_label = Label(self.intro_frame, text="{}/{}".format(self.questions_asked, self.num_questions),
                                 font=("Helvetica", 16))
        self.score_label.pack()

        # Label to display the quiz question
        self.question_label = Label(self.question_frame, text="", font=("Helvetica", 14), bg="#000000", fg="#FFFFFF",
                                    width=50, height=4)
        self.question_label.pack()

        # Buttons to select answers
        self.answer_buttons = [
            Button(self.answer_frame, text="", font=("Helvetica", 12), bg=self.color_map[weight_class], fg="#FFFFFF", width=20, height=2,
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

    # Function to get 4 unique boxers for the current round
    def get_round_boxers(self, weight_class_boxers):
        round_boxers_list = []
        while len(round_boxers_list) < 4:
            chosen_boxer = random.choice(weight_class_boxers)  # Randomly select a boxer
            if chosen_boxer not in round_boxers_list:  # Ensure the boxer is not already selected
                round_boxers_list.append(chosen_boxer)
        return round_boxers_list

    # Function to update the quiz with a new question
    def update_question(self):
        self.questions_asked += 1

        weight_class_boxers = self.all_boxers

        if not weight_class_boxers:
            # Handle error if no boxers are found for the selected weight class
            messagebox.showerror("Error", f"No boxers found for weight class '{self.weight_class}'.")
            self.root.destroy()
            return

        try:
            # Randomly select a boxer for the question
            boxer_info = random.choice(weight_class_boxers)
            boxer = boxer_info[0]
            reign_start = boxer_info[1]
            reign_end = boxer_info[2]
        except IndexError as e:
            # Handle error if there is an issue selecting a random boxer
            messagebox.showerror("Error", "There was an error selecting a random boxer.")
            self.root.destroy()
            return

        self.correct_boxer = boxer  # Set the correct answer for the current question
        self.question_label.config(text=f"Who became undisputed {self.weight_class} champion in {reign_start}?")

        # Get 4 boxers for the answer choices
        round_boxers = self.get_round_boxers(weight_class_boxers)
        if self.correct_boxer not in [boxer[0] for boxer in round_boxers]:
            round_boxers[random.randint(0, 3)][0] = self.correct_boxer  # Ensure the correct answer is among the choices

        random.shuffle(round_boxers)  # Randomize the order of answer choices

        # Set the text for the answer buttons
        for btn, boxer_info in zip(self.answer_buttons, round_boxers):
            btn.config(text=boxer_info[0])

        # Update the score label with the current progress
        self.score_label.config(text=f"{self.questions_asked}/{self.num_questions}")

    # Function to check if the selected answer is correct
    def check_answer(self, index):
        selected_name = self.answer_buttons[index].cget("text")
        if selected_name == self.correct_boxer:
            self.score += 1  # Increment score if the answer is correct
            messagebox.showinfo("Correct!", "That's the correct answer!")
        else:
            messagebox.showerror("Wrong!", f"The correct answer was {self.correct_boxer}")

        # Continue to the next question or end the quiz
        if self.questions_asked < self.num_questions:
            self.update_question()
        else:
            global attempts_data
            attempts_data.append({"questions_asked": self.num_questions, "correct_answers": self.score})
            self.show_end_screen()  # Show the end screen with final results

    # Function to show the end screen after the quiz is completed
    def show_end_screen(self):
        self.intro_frame.destroy()
        self.question_frame.destroy()
        self.answer_frame.destroy()
        EndScreen(self.root)


# Class to display the end screen with final results and options
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

        # Display result text based on the player's performance
        result_text, message_colour = self.get_result_text()
        self.congrats_label = Label(self.intro_frame, text=result_text, font=("Arial", 24), fg=message_colour)
        self.congrats_label.pack()

        # Display the final score
        self.score_label = Label(self.intro_frame, text="You got {} / {}".format(attempts_data[-1]
                                                                                     ["correct_answers"],
                                                                                     attempts_data[-1]
                                                                                     ["questions_asked"]),
                                 font=("Arial", 14), fg=message_colour)
        self.score_label.pack()

        self.winner_frame = Frame(self.frame, pady=10)
        self.winner_frame.grid(row=1, columnspan=3)

        # Display an image (e.g., a winner's belt) on the end screen
        self.winner_image = PhotoImage(file="Winner_Belt.png")  # Adjust path as necessary
        self.winner_label = Label(self.winner_frame, image=self.winner_image)
        self.winner_label.pack()

        # Keep a reference to the image to prevent garbage collection
        self.winner_label.image = self.winner_image

        self.buttons_frame = Frame(self.frame, pady=10)
        self.buttons_frame.grid(row=2, columnspan=3)

        # Button to view quiz statistics
        self.stats_button = Button(self.buttons_frame, text="Stats", bg="#330066", fg="#FFFFFF", font=button_font,
                                   width=13, height=2, command=lambda: DisplayStats(self, attempts_data))
        self.stats_button.grid(row=0, column=0, padx=10)

        # Button to start a new quiz
        self.play_again_button = Button(self.buttons_frame, text="Play Again", bg="#006600", fg="#FFFFFF",
                                        font=button_font, width=13, height=2, command=self.play_again)
        self.play_again_button.grid(row=0, column=1, padx=10)

        # Button to exit the application
        self.exit_button = Button(self.buttons_frame, text="Exit", bg="#990000", fg="#FFFFFF", font=button_font,
                                  width=13, height=2, command=self.root.quit)
        self.exit_button.grid(row=0, column=2, padx=10)

    # Function to generate the result text based on the player's score
    def get_result_text(self):
        last_attempt = attempts_data[-1]
        correct_answers = last_attempt["correct_answers"]
        questions_asked = last_attempt["questions_asked"]
        percentage = (correct_answers / questions_asked) * 100

        if percentage == 100:
            message_colour = "#006600"
            return "You are UNDISPUTED CHAMP!!", message_colour
        elif 50 <= percentage < 100:
            message_colour = "#006600"
            return "You are Unified Champ!", message_colour
        else:
            message_colour = "#990000"
            return "Oh No! Try again!", message_colour

    # Function to start a new quiz
    def play_again(self):
        self.frame.destroy()
        ChooseWeight(self.root)


# Main routine to start the application
if __name__ == "__main__":
    root = Tk()
    ChooseWeight(root)
    root.mainloop()
