"""Implements a QuizScorer class."""
import logging
import os
import yaml
import pandas as pd
from plot_utils import generate_plot

logging.basicConfig(level=20)
logger = logging.getLogger(__name__)

# pylint:disable=too-many-instance-attributes
class QuizScorer:
    """An aggregator and visualizer for quiz scores."""

    def __init__(self):
        """Instantiates a QuizScorer."""
        with open("../conf/config.yml") as file:
            config = yaml.full_load(file)
        self.correct_answers = pd.read_csv(
            "../scoring/correct_answers.csv", index_col="Name"
        )
        self.answers_dir = "../scoring/answers"
        self.answers = None
        self.outputs_dir = "../outputs"
        self.names = []
        self.scores = []
        self.ncorrect_matrix = None
        self.mock_scores = config.get("mock_scores")
        self.palette = config.get("palette", "Blues")
        self.dpi = config.get("dpi", 150)
        self.bands = config.get("bands")
        self.x_offset_plot = 0.1
        self.plot_title = "Game scores"

    def generate_scores(self):
        """Runs end-to-end scores processing."""
        self._fetch_answers()
        self._process_answers()
        self._save_ncorrect_matrix()
        self._build_scores_plot()

    def generate_mock_plot(self):
        """Creates and saves a mock template plot for debugging/explanatory purposes."""
        generate_plot(
            list(self.mock_scores.keys()),
            list(self.mock_scores.values()),
            self.outputs_dir,
            title="Sample scores output",
            bands=self.bands,
            dpi=self.dpi,
            palette=self.palette,
        )

    def _build_scores_plot(self):
        """Creates and saves a plot with all scores."""
        generate_plot(
            self.names,
            self.scores,
            self.outputs_dir,
            bands=self.bands,
            dpi=self.dpi,
            palette=self.palette,
        )

    def _fetch_answers(self):
        """Retrieves csv responses from `scoring/answers` directory."""
        answers = {}
        owd = os.getcwd()
        os.chdir(self.answers_dir)
        for file in os.listdir():
            name = os.path.splitext(file)[0]  # Strip file extension
            answers[name] = pd.read_csv(file, index_col="Name")
        os.chdir(owd)
        self.answers = answers

    def _process_answers(self):
        """Scores each answer against the template from `scoring/correct_answers.csv"""
        self.ncorrect_matrix = pd.DataFrame(
            index=self.correct_answers.index, columns=self.correct_answers.columns
        ).fillna(0)
        for name, answer in self.answers.items():
            guessed = answer == self.correct_answers
            self.scores.append(guessed.sum().sum())
            self.names.append(name)
            self.ncorrect_matrix = self.ncorrect_matrix.add(guessed)

    def _save_ncorrect_matrix(self):
        """Saves a matrix with the number of correct guesses per field and category."""
        save_path = f"{self.outputs_dir}/ncorrect_matrix.csv"
        self.ncorrect_matrix.to_csv(f"{self.outputs_dir}/ncorrect_matrix.csv")
        logger.info("Matrix with number of correct guesses saved to %s", save_path)


if __name__ == "__main__":
    scorer = QuizScorer()
    scorer.generate_scores()
    scorer.generate_mock_plot()
