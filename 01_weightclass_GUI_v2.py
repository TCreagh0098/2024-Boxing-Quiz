from tkinter import *
from functools import partial  # To prevent unwanted windows


class ChooseWeight:

    def __init__(self):

        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # set up GUI frame
        self.intro_frame = Frame(padx=50, pady=60)
        self.intro_frame.grid()

        # heading and brief instructions
        self.temp_heading = Label(self.intro_frame,
                                  text="Undisputed Boxing Champions Quiz",
                                  font=("Arial", "16", "bold"))

        self.temp_heading.grid(row=0)

        choose_instruction_txt = "\n\nThis quiz will test your boxing" \
                                 "knowledge by giving you a date that" \
                                 "a boxer became the undisputed " \
                                 "champion, you will then be provided " \
                                 "with four possible answers in the form " \
                                 "of a multi-choice question with one " \
                                 "answer being correct...\n\n" \
                                 "After completing the quiz you " \
                                 "will get a score out of how many " \
                                 "questions you got correct e.g. " \
                                 "6/10 or 13/20 etc...\n\n" \
                                 "To begin, please choose what " \
                                 "weight-class you want to be quizzed on..."

        self.choose_instructions_label = Label(self.intro_frame,
                                               text=choose_instruction_txt,
                                               wraplength=400,
                                               justify="left")
        self.choose_instructions_label.grid(row=1)

        # rounds buttons...
        self.which_weight_frame = Frame(self.intro_frame)
        self.which_weight_frame.grid(row=2)

        self.heavy_button = Button(self.which_weight_frame, fg=button_fg,
                                   bg="#990000", text="Heavyweight",
                                   font=button_font, width=13, height=2)
        self.heavy_button.grid(row=0, column=0, padx=5, pady=5)

        self.middle_button = Button(self.which_weight_frame, fg=button_fg,
                                    bg="#006600", text="Middleweight",
                                    font=button_font, width=13, height=2)
        self.middle_button.grid(row=0, column=1, padx=10, pady=10)

        self.light_button = Button(self.which_weight_frame, fg=button_fg,
                                   bg="#330066", text="Lightweight",
                                   font=button_font, width=13, height=2)
        self.light_button.grid(row=0, column=2, padx=5, pady=5)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Undisputed Quiz")
    ChooseWeight()
    root.mainloop()
