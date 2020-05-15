class Question:
    def __init__(self, category, question, number):
        self.category = category
        self.question = question
        self.number = number

    def get_question(self):
        return self.question

    def get_category(self):
        return self.category

    def get_number(self):
        return self.number


class Answer:
    def __init__(self, text, is_correct, question_number):
        self.text = text
        self.isCorrect = is_correct
        self.questionNumber = question_number

    def get_text(self):
        return self.text

    def is_correct(self):
        return self.isCorrect

    def get_question_number(self):
        return self.questionNumber
