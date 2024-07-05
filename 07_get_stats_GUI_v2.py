from tkinter import *
from functools import partial  # To prevent unwanted windows

# Sample data to simulate attempts history
attempts_data = [
    {"questions_asked": 10, "correct_answers": 7},
    {"questions_asked": 15, "correct_answers": 10},
    {"questions_asked": 20, "correct_answers": 18},
    {"questions_asked": 5, "correct_answers": 4},
    {"questions_asked": 12, "correct_answers": 6},
    {"questions_asked": 8, "correct_answers": 5}
]


def calculate_stats(attempts):
    recent_attempts = attempts[-4:]
    total_questions = sum(attempt["questions_asked"] for attempt in attempts)
    total_correct_answers = sum(attempt["correct_answers"] for attempt in attempts)
    average_correct_percentage = round((total_correct_answers / total_questions) * 100) if total_questions > 0 else 0

    return {
        "recent_attempts": recent_attempts,
        "average_correct_percentage": average_correct_percentage,
        "total_correct_answers": total_correct_answers,
        "total_questions_asked": total_questions
    }


class ChooseRounds:

    def __init__(self):
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)
        root.withdraw()


class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)
            self.control_button_ref.append(self.make_control_button)

        self.to_stats_btn = self.control_button_ref[1]

    def to_do(self, action):
        if action == "get help":
            pass
        elif action == "get stats":
            DisplayStats(self, attempts_data)
        else:
            self.close_play()

    def close_play(self):
        root.destroy()


class DisplayStats:

    def __init__(self, partner, attempts):
        self.stats_box = Toplevel()
        stats_bg_colour = "#DAE8FC"
        partner.to_stats_btn.config(state=DISABLED)
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame, text="Statistics", font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=0)

        stats_text = "Here are your game statistics"
        self.help_text_label = Label(self.stats_frame, text=stats_text, wraplength=350, justify="left",
                                     bg=stats_bg_colour)
        self.help_text_label.grid(row=1, padx=10)

        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, padx=10, pady=10)

        stats_output = calculate_stats(attempts)
        recent_attempts = stats_output["recent_attempts"]

        Label(self.data_frame, text="", bg="#FFFFFF", width=10, height=2, padx=5).grid(row=0, column=0)
        Label(self.data_frame, text="Attempt", bg="#FFFFFF", width=10, height=2, padx=5).grid(row=0, column=1)
        Label(self.data_frame, text="Score", bg="#FFFFFF", width=10, height=2, padx=5).grid(row=0, column=2)

        for idx, attempt in enumerate(recent_attempts):
            row_bg = "#C9D6E8" if idx % 2 == 0 else stats_bg_colour
            Label(self.data_frame, text=f"{idx + 1}", bg=row_bg, width=10, height=2, padx=5).grid(row=idx + 1, column=0)
            Label(self.data_frame, text=f"{attempt['questions_asked']} / {attempt['correct_answers']}", bg=row_bg,
                  width=10, height=2, padx=5).grid(row=idx + 1, column=1)
            Label(self.data_frame, text=f"{round(attempt['correct_answers'] / attempt['questions_asked'] * 100)}%",
                  bg=row_bg, width=10, height=2, padx=5).grid(row=idx + 1, column=2)

        Label(self.data_frame, text="Average Percentage", bg="#FFFFFF", width=10, height=2, padx=5).grid(
            row=len(recent_attempts) + 1, column=0)
        Label(self.data_frame, text=f"{stats_output['average_correct_percentage']}%", bg="#C9D6E8", width=10, height=2,
              padx=5).grid(row=len(recent_attempts) + 1, column=1)

        Label(self.data_frame, text="Total Questions", bg="#FFFFFF", width=10, height=2, padx=5).grid(
            row=len(recent_attempts) + 2, column=0)
        Label(self.data_frame, text=f"{stats_output['total_questions_asked']}", bg="#C9D6E8", width=10, height=2,
              padx=5).grid(row=len(recent_attempts) + 2, column=1)

        Label(self.data_frame, text="Total Correct", bg="#FFFFFF", width=10, height=2, padx=5).grid(
            row=len(recent_attempts) + 3, column=0)
        Label(self.data_frame, text=f"{stats_output['total_correct_answers']}", bg="#C9D6E8", width=10, height=2,
              padx=5).grid(row=len(recent_attempts) + 3, column=1)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "12", "bold"), text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=3, padx=10, pady=10)

    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Quiz Statistics")
    ChooseRounds()
    root.mainloop()
