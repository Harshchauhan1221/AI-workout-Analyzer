import matplotlib.pyplot as plt


def generate_report(exercise, reps, rep_accuracy, feedback):

    avg_accuracy = sum(rep_accuracy) / len(rep_accuracy) if rep_accuracy else 0

    # -------- TEXT REPORT --------
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Exercise: {exercise}\n")
        f.write(f"Total Reps: {reps}\n")
        f.write(f"Average Accuracy: {avg_accuracy:.2f}%\n")

        f.write("\nFeedback Summary:\n")
        for fb in set(feedback):
            f.write(f"- {fb}\n")

    # -------- REP-BASED GRAPH --------
    plt.figure()

    plt.plot(rep_accuracy, marker='o')

    plt.title(f"{exercise} Accuracy Per Rep")
    plt.xlabel("Rep Number")
    plt.ylabel("Accuracy (%)")

    plt.xticks(range(len(rep_accuracy)))
    plt.grid()

    plt.savefig(f"{exercise}_rep_graph.png")
    plt.close()