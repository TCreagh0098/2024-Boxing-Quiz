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
    recent_attempts = attempts[-4:]
    total_questions = sum(attempt["questions_asked"] for attempt in attempts)
    total_correct_answers = sum(attempt["correct_answers"] for attempt in attempts)

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
        self.stats_box = Toplevel()

        stats_bg_colour = "#FFFFFF"
        partner.to_stats_btn.config(state=DISABLED)
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame, text="Statistics", font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=0)

        stats_text = "Here are your quiz statistics...\n\nYour last 4 attempts will be " \
                     "displayed here along with your average percentage and total answers..."
        self.help_text_label = Label(self.stats_frame, text=stats_text, wraplength=350, justify="left",
                                     bg=stats_bg_colour)
        self.help_text_label.grid(row=1, padx=10, pady=10)

        self.data_frame = Frame(self.stats_frame, bg="#FFFFFF", borderwidth=1, relief="solid", height="80")
        self.data_frame.grid(row=2, column=1, padx=2, pady=2)

        stats_output = stats(attempts)
        recent_attempts = stats_output["recent_attempts"]
        average_correct_percentage = stats_output["average_correct_percentage"]
        total_correct_answers = stats_output["total_correct_answers"]
        total_questions_asked = stats_output["total_questions_asked"]

        head_back = "#990000"
        odd_rows = "#990000"
        even_rows = "#990000"

        row_names = ["", "Total Questions Asked", "Total Correct Answers", "Average Correct Percentage"]
        row_formats = [head_back, odd_rows, even_rows, odd_rows]

        all_labels = []
        all_labels.append([row_names[1], row_formats[1]])
        all_labels.append([total_questions_asked, row_formats[1]])
        all_labels.append([row_names[2], row_formats[2]])
        all_labels.append([total_correct_answers, row_formats[2]])
        all_labels.append([row_names[3], row_formats[3]])
        all_labels.append(["{}%".format(average_correct_percentage), row_formats[3]])

        for item in range(len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0], bg=all_labels[item][1], borderwidth=1,
                                    width="20", relief="solid",
                                    height="2", padx=5, fg="#FFFFFF")
            self.data_label.grid(row=item // 2, column=item % 2, padx=0, pady=0)

        self.recent_attempts_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid",
                                           width="10",)
        self.recent_attempts_frame.grid(row=2, column=0, padx=5, pady=5)

        # Display recent attempts as "questions asked / correct answers"
        all_attempts_labels = []
        count = 1
        for attempt in recent_attempts:
            attempt_text = "{} / {}".format(attempt['questions_asked'], attempt['correct_answers'])
            all_attempts_labels.append([attempt_text, head_back])
            count += 1

        for item in range(len(all_attempts_labels)):
            self.attempts_data_label = Label(self.recent_attempts_frame, text=all_attempts_labels[item][0],
                                             bg=all_attempts_labels[item][1], width="20", height="2", padx=5,
                                             borderwidth=1, relief="solid",
                                             fg="#FFFFFF")
            self.attempts_data_label.grid(row=item, column=0, padx=0, pady=0)

    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main root window
    root.title("Undisputed Quiz")

    class DummyPartner:
        def __init__(self):
            self.to_stats_btn = Button(root)


    partner = DummyPartner()
    DisplayStats(partner, attempts_data)
    root.mainloop()
