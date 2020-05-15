#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from quiz import Quiz
from file_handler import FileHandler


categories = ['Maantieto', 'Tiede']
categories_map = {'Maantieto': 'geo', 'Tiede': 'science'}


class ButtonBlock(ttk.Frame):
    def __init__(self, parent, button_content, columns, answers=True):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []
        if answers:
            self.answers = button_content
            for i, answer in enumerate(self.answers):
                self.buttons.append(ttk.Button(self, text=answer.get_text(), command=lambda i=i: self.get_answer(i), width=15))
                self.buttons[i].grid(row=i // columns, column=i % columns, sticky=tk.W + tk.E + tk.S + tk.N, pady=10,
                                     padx=10)
        else:
            self.categories = button_content
            for i, category in enumerate(self.categories):
                self.buttons.append(ttk.Button(self, text=category, command=lambda i=i: self.get_category(i), width=15))
                self.buttons[i].grid(row=i // columns, column=i % columns, sticky=tk.W + tk.E + tk.S + tk.N, pady=10,
                                     padx=10)

    def get_answer(self, num):
        self.parent.check_answer(self.answers[num].isCorrect)

    def get_category(self, num):
        category = categories_map[self.buttons[num]['text']]
        self.parent.create_quiz(category)


class UI(tk.Tk):
    def __init__(self, title="QuizMaster"):
        super().__init__()
        self.title(title)
        self.geometry("720x300")
        self.__quiz = None
        self.question = tk.StringVar()
        self.info = tk.StringVar()
        self.question_frame = tk.Frame(self).grid(row=1, sticky=tk.W + tk.E + tk.S + tk.N)
        tk.Label(self.question_frame, textvariable=self.question).grid(padx=75, pady=20,
                                                                      sticky=tk.W + tk.E + tk.S + tk.N, columnspan=5)

        self.buttons = ButtonBlock(self, categories, 2, answers=False)
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=6, column=2, padx=20, pady=15, sticky=tk.W + tk.E + tk.S + tk.N)
        tk.Label(self.info_frame, textvariable=self.info).pack(side=tk.LEFT, padx=40)

        self.canvas = tk.Canvas(self, width=500, height=200)
        self.canvas.grid(row=12, columnspan=9, padx=120, sticky=tk.W + tk.E + tk.S + tk.N)

        self.protocol("WM_DELETE_WINDOW", self.close)

        if os.path.exists('db/games/quiz.dat'):
            msq = messagebox.askquestion("Lataa peli", "Haluatko jatkaa viimeksi tallennettua peliä?")
            if msq == 'yes':
                f = FileHandler()
                self.__quiz = f.deserialize()
                self.__quiz.loaded_game_question = self.__quiz.questionToAsk
                self.start_quiz()
            else:
                os.remove('db/games/quiz.dat')
                self.create_start_menu()
        else:
            self.create_start_menu()

    def create_start_menu(self):
        self.question.set('Tervetuloa pelaamaan QuizMasteria.\nAloita valitsemalla kategoria.')
        self.buttons = ButtonBlock(self, categories, 2, answers=False)
        self.buttons.grid(row=4, column=0, columnspan=3, padx=200, pady=5)

    def create_quiz(self, category):
        self.__quiz = Quiz(category)
        self.start_quiz()

    def start_quiz(self):
        self.buttons.destroy()
        self.question.set(self.__quiz.ask_question())
        self.buttons = ButtonBlock(self, self.__quiz.ansForQuestion, 2)
        self.buttons.grid(row=4, column=0, columnspan=3, padx=200, pady=5)
        self.create_circles()
        self.fill_circles(fill_many=True)

    def create_circles(self):
        start = 5
        end = 25
        for i in range(len(self.__quiz.questions)):
            self.canvas.create_oval(start, 5, end, 25, width=2)
            start += 30
            end += 30

    def fill_circles(self, fill_many=False):
        if not fill_many:
            start = 5 + 30 * self.__quiz.questionToAsk
            end = 25 + 30 * self.__quiz.questionToAsk
            if self.__quiz.result_map[self.__quiz.questionToAsk]:
                self.canvas.create_oval(start, 5, end, 25, width=2, fill='#1d5e2b')
            else:
                self.canvas.create_oval(start, 5, end, 25, width=2, fill='#b50b0b')
        else:
            for i in range(self.__quiz.questionToAsk):
                start = 5 + 30 * i
                end = 25 + 30 * i
                if self.__quiz.result_map[i]:
                    self.canvas.create_oval(start, 5, end, 25, width=2, fill='#1d5e2b')
                else:
                    self.canvas.create_oval(start, 5, end, 25, width=2, fill='#b50b0b')
            if self.__quiz.questionToAsk == len(self.__quiz.questions) - 1:
                self.fill_circles()

    def check_answer(self, is_correct):
        if is_correct:
            self.__quiz.corrects += 1
            self.__quiz.result_map[self.__quiz.questionToAsk] = True
            self.fill_circles()
        else:
            self.__quiz.result_map[self.__quiz.questionToAsk] = False
            self.fill_circles()
        if self.__quiz.questionToAsk < len(self.__quiz.questions) - 1:
            self.__quiz.questionToAsk += 1
            self.ask_new_question()
        else:
            self.info.set(f"Peli päättyi! Tiesit oikein {self.__quiz.corrects} / {len(self.__quiz.questions)}")
            tk.Button(self.info_frame, text='Aloita uusi peli', command=self.new_game).pack(side=tk.LEFT, padx=40)
            self.buttons.destroy()
            self.question.set("")

    def ask_new_question(self):
        self.question.set(self.__quiz.ask_question())
        self.__quiz.get_answers_for_question(self.__quiz.questionToAsk)
        self.buttons.grid_forget()
        self.buttons = ButtonBlock(self, self.__quiz.ansForQuestion, 2)
        self.buttons.grid(row=4, column=0, columnspan=3, padx=200, pady=5)

    def close(self):
        """
        * game cannot be saved in:
            -"start menu"
            - if all the questions are answered
            - if player hasn't answered to any new question
        """
        if self.__quiz is not None:
            if self.__quiz.result_map.get(len(self.__quiz.questions) - 1) is None and self.__quiz.loaded_game_question != self.__quiz.questionToAsk:
                msg_box = messagebox.askquestion("Tallenna", "Haluatko tallentaa pelin ennen sulkemista?", icon='warning')
                if msg_box == "yes":
                    f = FileHandler()
                    f.serialize(self.__quiz)
        self.destroy()

    def new_game(self):
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=6, column=2, padx=20, pady=15, sticky=tk.W + tk.E + tk.S + tk.N)
        tk.Label(self.info_frame, textvariable=self.info).pack(side=tk.LEFT, padx=40)
        self.info.set('')
        self.canvas.destroy()
        self.canvas = tk.Canvas(self, width=500, height=200)
        self.canvas.grid(row=12, columnspan=9, padx=120, sticky=tk.W + tk.E + tk.S + tk.N)
        self.create_start_menu()
        self.__quiz = None


if __name__ == '__main__':
    ui = UI()
    ui.mainloop()
