import os
import pickle
import pandas as pd


def fetch_answers():
    answers = {}
    os.chdir("../scoring/answers")
    for file in os.listdir():
        name = os.path.splitext(file)[0]  # Strip file extension
        answers[name] = pd.read_csv(file, index_col="Name")
    return answers


def calculate_correct(answers, correct_answers):
    scores = {}
    correct_guesses_matrix = pd.DataFrame(
        index=correct_answers.index, columns=correct_answers.columns
    ).fillna(0)
    for name, answer in answers.items():
        guessed = answer == correct_answers
        scores[name] = (guessed).sum().sum()
        correct_guesses_matrix = correct_guesses_matrix.add(guessed)

    return scores, correct_guesses_matrix


def compute_scores():
    owd = os.getcwd()
    correct_answers = pd.read_csv("../scoring/correct_answers.csv", index_col="Name")
    answers = fetch_answers()
    scores, correct_guesses_matrix = calculate_correct(answers, correct_answers)
    os.chdir(owd)
    return scores, correct_guesses_matrix


if __name__ == "__main__":
    scores_dict, correct_guesses_matrix = compute_scores()
    with open("../outputs/scores_dict.p", "wb") as f:
        pickle.dump(scores_dict, f)
    correct_guesses_matrix.to_csv("../outputs/correct_guesses_matrix.csv")
