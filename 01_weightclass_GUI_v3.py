from tkinter import *
from functools import partial  # To prevent unwanted windows
import random
from tkinter import messagebox

# Data for the quiz
weight_classes = {
    "heavyweight": [("Mike Tyson", "1986"), ("Lennox Lewis", "1999"), ("Wladimir Klitschko", "2006")],
    "middleweight": [("Sugar Ray Leonard", "1987"), ("Marvin Hagler", "1980"), ("Bernard Hopkins", "2001")],
    "lightweight": [("Roberto Durán", "1972"), ("Julio César Chávez", "1984"), ("Floyd Mayweather Jr.", "2002")]
}

class ChooseWeight:

    def __init__(self):
        button_font = ("Arial", "13", "bold")
        button_fg = "#FFFFFF"

        # set up GUI frame
        self.intro_frame = Frame(padx=50, pady=60)
        self.intro_frame.grid()

        #

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
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("Heavyweight", 28))
        self.heavy_button.grid(row=0, column=0, padx=5, pady=5)

        self.middle_button = Button(self.which_weight_frame, fg=button_fg,
                                    bg="#006600", text="Middleweight",
                                    font=button_font, width=13, height=2,
                                    command=lambda: self.weight_select("Middleweight", 40))
        self.middle_button.grid(row=0, column=1, padx=10, pady=10)

        self.light_button = Button(self.which_weight_frame, fg=button_fg,
                                   bg="#330066", text="Lightweight",
                                   font=button_font, width=13, height=2,
                                   command=lambda: self.weight_select("Lightweight", 31))
        self.light_button.grid(row=0, column=2, padx=5, pady=5)

    def weight_select(self, weight_class, max_rounds):
        # Create a new window
        new_window = Toplevel()
        new_window.title("Weight Class Selected")

        # Display the selected weight class and max rounds
        label = Label(new_window,
                      text=f"You have selected {weight_class}.\nMaximum rounds: {max_rounds}",
                      font=("Arial", 14))
        label.pack(padx=20, pady=20)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Undisputed Quiz")
    ChooseWeight()
    root.mainloop()
