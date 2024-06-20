from tkinter import *

# example values to see what it will look like in GUI
# will be replaced when integrated
user_score = 15
questions_answered = 20


# GUI for end screen
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

        self.buttons_frame = Frame(self.frame, pady=10)
        self.buttons_frame.grid(row=2, columnspan=3)

        self.stats_button = Button(self.buttons_frame, text="Stats", bg="#330066", fg="#FFFFFF", font=button_font,
                                   width=13, height=2)
        self.stats_button.grid(row=0, column=0, padx=10)

        self.play_again_button = Button(self.buttons_frame, text="Play Again", bg="#006600", fg="#FFFFFF",
                                        font=button_font, width=13, height=2)
        self.play_again_button.grid(row=0, column=1, padx=10)

        self.exit_button = Button(self.buttons_frame, text="Exit", bg="#990000", fg="#FFFFFF", font=button_font,
                                  width=13, height=2, command=self.root.quit)
        self.exit_button.grid(row=0, column=2, padx=10)


# Main routine
if __name__ == "__main__":
    root = Tk()
    app = EndScreen(root)
    root.mainloop()
