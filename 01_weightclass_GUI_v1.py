from tkinter import *

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


class Statistics:
    def __init__(self, parent):
        self.stats_frame = Frame(parent, padx=50, pady=60)
        self.stats_frame.grid()

        stats_output = stats(attempts_data)

        # Display statistics
        Label(self.stats_frame, text="Statistics", font=("Arial", "16", "bold")).grid(row=0, columnspan=2)

        recent_attempts_text = "\n".join(
            [f"{attempt['correct_answers']} / {attempt['questions_asked']}" for attempt in
             stats_output["recent_attempts"]]
        )
        Label(self.stats_frame, text=recent_attempts_text, bg="#990000", fg="#FFFFFF",
              font=("Arial", 12), padx=10, pady=5).grid(row=1, column=0, sticky="nw")

        Label(self.stats_frame, text="Average Percentage", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=2, column=0, sticky="nw")
        Label(self.stats_frame, text=f"{stats_output['average_correct_percentage']}%", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12), padx=10, pady=5).grid(row=2, column=1, sticky="nw")

        Label(self.stats_frame, text="Total Questions Answered", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=3, column=0, sticky="nw")
        Label(self.stats_frame, text=f"{stats_output['total_questions_asked']}", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12), padx=10, pady=5).grid(row=3, column=1, sticky="nw")

        Label(self.stats_frame, text="Total Correct Answers", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=4, column=0, sticky="nw")
        Label(self.stats_frame, text=f"{stats_output['total_correct_answers']}", bg="#990000", fg="#FFFFFF",
              font=("Arial", 12), padx=10, pady=5).grid(row=4, column=1, sticky="nw")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz Statistics")
    Statistics(root)
    root.mainloop()
