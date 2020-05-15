from file_handler import FileHandler
from random import sample


class Quiz:
    def __init__(self, category):
        self.questionToAsk = 0
        self.loaded_game_question = 0
        self.questions = self.get_random_questions(category)
        self.answers = self.get_answers(self.questions)
        self.ansForQuestion = []
        self.corrects = 0
        self.get_answers_for_question(self.questionToAsk)
        self.result_map = {}

    @staticmethod
    def get_random_questions(category):
        f = FileHandler()
        questions = f.read_questions(category)
        random_questions = sample(questions, 15)
        return random_questions

    @staticmethod
    def get_answers(questions):
        f = FileHandler()
        answers = []
        for q in questions:
            answers_for_question = f.read_answers(q.get_category(), q.get_number())
            answers.append(answers_for_question)
        return answers

    def ask_question(self):
        """
        returns question text from a question
        """
        question = self.questions[self.questionToAsk]
        return question.get_question()

    def get_answers_for_question(self, questionToAsk):
        """
        * returns answer choices for currently active question
        """
        answers = []
        num = self.questions[questionToAsk].get_number()
        for tuples in self.answers:
            for answer in tuples:
                if answer.get_question_number() == num:
                    answers.append(answer)
        self.ansForQuestion = answers
