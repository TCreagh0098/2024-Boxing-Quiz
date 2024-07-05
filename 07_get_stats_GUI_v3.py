from tkinter import *
from functools import partial

# Sample data to simulate attempts history
attempts_data = [
    {"questions_asked": 10, "correct_answers": 7},
    {"questions_asked": 15, "correct_answers": 10},
    {"questions_asked": 20, "correct_answers": 18},
    {"questions_asked": 5, "correct_answers": 4},
    {"questions_asked": 12, "correct_answers": 6},
    {"questions_asked": 8, "correct_answers": 5}
]


def stats(attempts):
    # Get the four most recent attempts
    recent_attempts = attempts[-4:]

    # Calculate the total questions asked and total correct answers
    total_questions = sum(attempt["questions_asked"] for attempt in attempts)
    total_correct_answers = sum(attempt["correct_answers"] for attempt in attempts)

    # Calculate the average correct answer percentage and round it to a whole number
    if total_questions > 0:
        average_correct_percentage = round((total_correct_answers / total_questions) * 100)
    else:
        average_correct_percentage = 0

    return {
        "recent_attempts": recent_attempts,
        "average_correct_percentage": average_correct_percentage,
        "total_correct_answers": total_correct_answers,
        "total_questions_asked": total_questions
    }


class DisplayStats:
    def __init__(self, partner, attempts):
        # setup dialogue box and background colour
        self.stats_box = Toplevel()

        stats_bg_colour = "#DAE8FC"

        # disable help button
        partner.to_stats_btn.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=0)

        stats_text = "Here are your game statistics"
        self.help_text_label = Label(self.stats_frame, text=stats_text, wraplength=350,
                                     justify="left", bg=stats_bg_colour)
        self.help_text_label.grid(row=1, padx=10)

        # frame to hold statistics 'table'
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, padx=10, pady=10)

        stats_output = stats(attempts)

        # get statistics for user
        recent_attempts = stats_output["recent_attempts"]
        average_correct_percentage = stats_output["average_correct_percentage"]
        total_correct_answers = stats_output["total_correct_answers"]
        total_questions_asked = stats_output["total_questions_asked"]

        # background formatting for heading, odd and even rows
        head_back = "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = stats_bg_colour

        row_names = ["", "Total Questions Asked", "Total Correct Answers", "Average Correct Percentage"]
        row_formats = [head_back, odd_rows, even_rows, odd_rows]

        # data for labels (one label / sub list)
        all_labels = []

        all_labels.append([row_names[1], row_formats[1]])
        all_labels.append([total_questions_asked, row_formats[1]])
        all_labels.append([row_names[2], row_formats[2]])
        all_labels.append([total_correct_answers, row_formats[2]])
        all_labels.append([row_names[3], row_formats[3]])
        all_labels.append([f"{average_correct_percentage}%", row_formats[3]])

        # create labels based on list above
        for item in range(len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0],
                                    bg=all_labels[item][1],
                                    width="20", height="2", padx=5)
            self.data_label.grid(row=item // 2,
                                 column=item % 2,
                                 padx=0, pady=0)

        # Recent Attempts Section
        recent_attempts_heading = Label(self.stats_frame, text="Recent Attempts",
                                        font=("Arial", "12", "bold"),
                                        bg=stats_bg_colour)
        recent_attempts_heading.grid(row=3, pady=10)

        self.recent_attempts_frame = Frame(self.stats_frame, bg=stats_bg_colour,
                                           borderwidth=1, relief="solid")
        self.recent_attempts_frame.grid(row=4, padx=10, pady=10)

        attempts_row_names = ["Questions Asked", "Correct Answers"]
        attempts_row_formats = [head_back, odd_rows, even_rows, odd_rows]

        all_attempts_labels = []

        count = 0
        for attempt in recent_attempts:
            all_attempts_labels.append([f"Attempt {count + 1}", head_back])
            all_attempts_labels.append([attempts_row_names[0], attempts_row_formats[1]])
            all_attempts_labels.append([attempt["questions_asked"], attempts_row_formats[1]])
            all_attempts_labels.append([attempts_row_names[1], attempts_row_formats[2]])
            all_attempts_labels.append([attempt["correct_answers"], attempts_row_formats[2]])
            count += 1

        for item in range(len(all_attempts_labels)):
            self.attempts_data_label = Label(self.recent_attempts_frame, text=all_attempts_labels[item][0],
                                             bg=all_attempts_labels[item][1],
                                             width="20", height="2", padx=5)
            self.attempts_data_label.grid(row=item // 5,
                                          column=item % 5,
                                          padx=0, pady=0)

        # Dismiss button
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=5, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_stats(self, partner):
        # Put help button back to normal...
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


# Main routine to test the DisplayStats class
if __name__ == "__main__":
    root = Tk()
    root.title("Statistics Display Test")


    class DummyPartner:
        def __init__(self):
            self.to_stats_btn = Button(root)


    partner = DummyPartner()
    DisplayStats(partner, attempts_data)
    root.mainloop()
