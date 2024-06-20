from tkinter import *


class NumberQuestions:

    def __init__(self):
        # initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # common format for all buttons
        # arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # set up GUI frame
        self.question_frame = Frame(padx=60, pady=50)
        self.question_frame.grid()

        self.question_heading = Label(self.question_frame,
                                      text="Undisputed Quiz",
                                      font=("Arial", "16", "bold")
                                      )
        self.question_heading.grid(row=0)

        instructions = "To continue with the quiz please enter" \
                       "how many questions you wish to answer...\n\n" \
                       "Depending on which weight class you selected" \
                       "there will be a limit to how many questions" \
                       "can be generated...\n\n" \
                       "How many questions do you want to be generated..."
        self.question_instructions = Label(self.question_frame,
                                           text=instructions,
                                           wrap=250, width=40,
                                           justify="left")
        self.question_instructions.grid(row=1)

        self.question_entry = Entry(self.question_frame,
                                    font=("Arial", "14")
                                    )
        self.question_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.output_label = Label(self.question_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        # conversion, help and history / export buttons
        self.button_frame = Frame(self.question_frame)
        self.button_frame.grid(row=4)

        self.quiz_begin_button = Button(self.button_frame,
                                        text="Begin",
                                        bg="#006600",
                                        fg=button_fg,
                                        font=button_font, width=12)
        self.quiz_begin_button.grid(row=0, column=0, padx=5, pady=5)

# checks user input amd if it's valid, converts temperature
    def check_question(self, min_value, max_value):

        has_error = "no"

        # check that user has entered a valid number...

        response = self.question_entry.get()

        try:
            response = float(response)

            if min_value < response < max_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # sets var_has_error so that entry box and
        # labels can be correctly formatted by formatting function
        if has_error == "yes":
            error = "Please enter a number greater " \
                    "than {} and less than {}".format(min_value, max_value)

            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # if we have no errors...
        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")

            return response

    # shows user output and clears entry widget
    # ready for next calculation
    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000")
            self.question_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00")
            self.question_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Undisputed Quiz")
    NumberQuestions()
    root.mainloop()
