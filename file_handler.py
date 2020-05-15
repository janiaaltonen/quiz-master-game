from q_a import Question, Answer
import pickle


class FileHandler:
    def __init__(self):
        self.db_path = 'db/'
        self.save_path = self.db_path + 'games/'
        self.questions = '_questions.dat'
        self.answers = '_answers.dat'
        self.game_file = 'quiz.dat'

    def read_questions(self, category):
        filename = category + self.questions
        path = self.db_path + filename
        questions = []
        with open(path, 'r', encoding="utf-8") as file:
            number = 0
            for row in file:
                question = row.strip()
                if len(question) > 0:
                    q = Question(category, question, number)
                    questions.append(q)
                    number += 1
        file.close()
        return tuple(questions)

    def read_answers(self, category, number):
        filename = category + self.answers
        path = self.db_path + filename
        answers = []
        with open(path, 'r', encoding="utf-8") as file:
            for i, row in enumerate(file):
                if i == number:
                    options = row.strip().split(";")
                    for option in options:
                        if "=T" in option:
                            answer = option.split("=T")[0]
                            a = Answer(answer, True, number)
                            answers.append(a)
                        else:
                            a = Answer(option, False, number)
                            answers.append(a)
        file.close()
        return tuple(answers)

    def serialize(self, quiz_object):
        with open(self.save_path + self.game_file, 'bw+') as file:
            pickle.dump(quiz_object, file)
        if file is not None:
            file.close()

    def deserialize(self):
        with open(self.save_path + self.game_file, 'br') as file:
            quiz = pickle.load(file)
            if quiz is not None:
                return quiz
            return None
