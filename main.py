import csv
import random
from tkinter import *
from tkinter import font as tkfont
from tkinter import scrolledtext as st


class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        self.title("SAT Vocabs")
        self.geometry("550x400")
        self.resizable(False, False)

        self.title_font = tkfont.Font(family='Arial', size=25)
        self.big_font = tkfont.Font(family="Arial", size=15)
        self.medium_font = tkfont.Font(family="Arial", size=10)

        self.word_list = {}

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.f = "word_lists/words1.csv"
        self.read_word_file()

        self.bg_colour = 'white'
        self.button_colour = 'white'
        self.groove_colour = 'red'
        self.pad = 2

        for F in (HomePage, ProgressPage, WordsPage, MeaningsPage, SpellingsPage, SentencesPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            frame.rowconfigure((0, 1, 2), weight=1)
            frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if frame.__str__ == "ProgressPage":
            frame.display_words(self.word_list)
        elif frame.__str__ != "ProgressPage" and frame.__str__ != "HomePage":
            self.bind("<space>", frame.next_word)
        frame.tkraise()

    def read_word_file(self):
        with open(self.f, 'r', encoding="utf8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                word = row[0]
                form = row[1]
                definition = row[2]
                korean = row[3]
                example = row[4]
                related = row[5]
                status = row[6]
                self.word_list[word] = {"word": word, "form": form, "definition": definition, "korean": korean,
                                        "example": example,
                                        "related": related, "status": status}

    def save_word_list(self):
        fieldnames = ['word', 'form', 'definition', 'korean', 'example', 'related', 'status']
        with open(self.f, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.word_list.values())


class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.bg_colour)
        self.__str__ = "HomePage"

        ###### SETTINGS #######
        pad = controller.pad

        ########## WIDGETS #########
        label = Label(self, text="SAT Vocab", width=5, bg=controller.bg_colour, font=controller.title_font)

        progress_btn = Button(self, text="📊", font=controller.big_font,
                              highlightbackground=controller.groove_colour,
                              bg=controller.button_colour, relief="groove",
                              command=lambda: controller.show_frame("ProgressPage"))
        words_btn = Button(self, text="Words", width=5, font=controller.big_font, bg=controller.button_colour,
                           relief="groove",
                           command=lambda: controller.show_frame("WordsPage"))
        meanings_btn = Button(self, text="Meanings", width=5, font=controller.big_font, bg=controller.button_colour,
                              relief="groove",
                              command=lambda: controller.show_frame("MeaningsPage"))
        spellings_btn = Button(self, text="Spellings", width=5, font=controller.big_font, bg=controller.button_colour,
                               relief="groove",
                               command=lambda: controller.show_frame("SpellingsPage"))
        sentences_btn = Button(self, text="Sentences", width=5, font=controller.big_font, bg=controller.button_colour,
                               relief="groove",
                               command=lambda: controller.show_frame("SentencesPage"))

        ########## PLACEMENTS ###########
        progress_btn.place(x=410, y=45)
        label.grid(row=0, column=1, columnspan=2, sticky="nsew")
        words_btn.grid(row=1, column=0, columnspan=2, padx=pad, pady=pad, sticky="nsew")
        meanings_btn.grid(row=1, column=2, columnspan=2, padx=pad, pady=pad, sticky="nsew")
        spellings_btn.grid(row=2, column=0, columnspan=2, padx=pad, pady=pad, sticky="nsew")
        sentences_btn.grid(row=2, column=2, columnspan=2, padx=pad, pady=pad, sticky="nsew")


class ProgressPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.__str__ = "ProgressPage"
        self.controller = controller
        self.configure(bg=controller.bg_colour)

        ######### SETTINGS #########
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)
        pad = controller.pad

        ######## WIDGETS #########
        self.search_query = MutableText(self, font=controller.big_font, width=10, height=1, relief="groove")

        home_btn = Button(self, text="←", font=controller.big_font, bg=controller.button_colour,
                          relief="groove",
                          command=lambda: controller.show_frame("HomePage"))

        red_btn = Button(self, text="😟", font=controller.big_font, bg='red',
                         relief="groove",
                         command=lambda: self.filter_search("R"))

        amber_btn = Button(self, text="😐", font=controller.big_font, bg='orange',
                           relief="groove",
                           command=lambda: self.filter_search("A"))

        green_btn = Button(self, text="😄", font=controller.big_font, bg='green',
                           relief="groove",
                           command=lambda: self.filter_search("G"))

        new_btn = Button(self, text="😎", font=controller.big_font, bg='blue',
                         relief="groove",
                         command=lambda: self.filter_search(""))

        self.word_list_box = Listbox(self, font=controller.big_font, width=10)

        self.word_text_box = st.ScrolledText(self, font=controller.big_font, bg=controller.button_colour, width=10,
                                             height=10, wrap="word", exportselection=False,
                                             relief="groove")

        ########### PLACEMENTS ##########3
        home_btn.place(x=pad, y=pad)

        red_btn.grid(row=0, column=1, padx=pad, pady=pad, sticky="sew")
        amber_btn.grid(row=0, column=2, padx=pad, pady=pad, sticky="sew")
        green_btn.grid(row=0, column=3, padx=pad, pady=pad, sticky="sew")
        new_btn.grid(row=0, column=4, padx=pad, pady=pad, sticky="sew")

        self.search_query.grid(row=0, column=0, padx=pad, pady=pad, sticky="sew")
        self.word_list_box.grid(row=1, column=0, rowspan=2, padx=pad, pady=pad, sticky="nsew")
        self.word_text_box.grid(row=1, column=1, rowspan=2, padx=pad, pady=pad, columnspan=4, sticky="nsew")

        ######### BINDS / PRESETS ########
        self.search_query.bind("<<TextModified>>", self.text_modified)
        self.word_list_box.bind("<<ListboxSelect>>", self.listbox_select)
        self.display_words(controller.word_list.keys())

    def display_words(self, l):
        self.word_list_box.delete(0, END)
        for word in l:
            self.word_list_box.insert(END, word)
            status = self.controller.word_list[word]['status']
            if status == "R":
                self.word_list_box.itemconfig(END, {"fg": "red", "selectforeground": "red",
                                                    "selectbackground": "#ffe0e0"})
            elif status == "A":
                self.word_list_box.itemconfig(END, {"fg": "orange", "selectforeground": "orange",
                                                    "selectbackground": "#fff3e0"})
            elif status == "G":
                self.word_list_box.itemconfig(END, {"fg": "green", "selectforeground": "green",
                                                    "selectbackground": "#e0ffe2"})
            elif status == "":
                self.word_list_box.itemconfig(END, {"fg": "blue", "selectforeground": "blue",
                                                    "selectbackground": "#e0eeff"})
            else:
                pass

    def filter_search(self, c):
        temp = []
        for word in self.controller.word_list.keys():
            if self.controller.word_list[word]['status'] == c:
                temp.append(word)

        self.display_words(temp)

    def text_modified(self, event):
        chars = event.widget.get("1.0", "end-1c")
        temp = []
        if chars != "":
            for word in self.controller.word_list.keys():
                if chars in word:
                    temp.append(word)
            self.display_words(temp)
        else:
            self.display_words(self.controller.word_list.keys())

    def listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            word = event.widget.get(index)
            t = f"""
{self.controller.word_list[word]['form']} {word}
{self.controller.word_list[word]['related'] if self.controller.word_list[word]['related'] != "." else ""} 

{self.controller.word_list[word]['definition']} 
{self.controller.word_list[word]['korean']}
  
{self.controller.word_list[word]['example']} 
  
"""
            self.word_text_box.configure(state=NORMAL)
            self.word_text_box.delete(1.0, END)
            self.word_text_box.insert(INSERT, t, ("centered",))
            self.word_text_box.tag_configure("centered", justify="center")
            self.word_text_box.configure(state=DISABLED)
        else:
            self.word_text_box.configure(state=NORMAL)
            self.word_text_box.delete(1.0, END)
            self.word_text_box.configure(state=DISABLED)


class WordsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.bg_colour)
        self.__str__ = "WordsPage"

        ####### SETTINGS ########
        pad = controller.pad
        self.current_answer = ""
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.take_answer = True
        self.answer_btn = None

        ####### WIDGETS #######
        home_btn = Button(self, text="←", font=controller.big_font, bg=controller.button_colour,
                          relief="groove",
                          command=lambda: controller.show_frame("HomePage"))

        self.question_label = Label(self, text="", width=1, wraplength=412, bg=controller.bg_colour,
                                    font=controller.title_font)

        self.ans1_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans1_btn.configure(command=lambda btn=self.ans1_btn: self.submit_answer(btn))

        self.ans2_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans2_btn.configure(command=lambda btn=self.ans2_btn: self.submit_answer(btn))

        self.ans3_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans3_btn.configure(command=lambda btn=self.ans3_btn: self.submit_answer(btn))

        self.ans4_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans4_btn.configure(command=lambda btn=self.ans4_btn: self.submit_answer(btn))

        next_question = Button(self, text="Next", width=5, font=controller.big_font, bg=controller.button_colour,
                               relief="groove", command=self.next_word)

        ####### PLACEMENTS #######
        home_btn.place(x=pad, y=pad)
        self.question_label.grid(row=0, column=1, columnspan=6, sticky="nsew")
        self.ans1_btn.grid(row=1, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans2_btn.grid(row=1, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans3_btn.grid(row=2, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans4_btn.grid(row=2, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        next_question.place(x=482, y=93)

        ########## BINDS / PRESETS ########
        self.next_word()

    def next_word(self, e=0):
        sample = random.sample(list(self.controller.word_list.keys()), 4)
        self.current_answer = random.choice(sample)
        self.question_label['text'] = self.controller.word_list[self.current_answer]['definition']
        self.ans1_btn['text'] = sample[0]
        self.ans2_btn['text'] = sample[1]
        self.ans3_btn['text'] = sample[2]
        self.ans4_btn['text'] = sample[3]

        for btn in (self.ans1_btn, self.ans2_btn, self.ans3_btn, self.ans4_btn):
            btn.configure(bg="white", activebackground="SystemButtonFace")
            if btn['text'] == self.current_answer:
                self.answer_btn = btn
        self.take_answer = True

    def submit_answer(self, b):
        if self.take_answer:
            ans = b['text']
            if ans == self.current_answer:
                b['bg'] = 'green'
                b['activebackground'] = 'green'
                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "G"
                elif status == "G":
                    pass
                else:
                    self.controller.word_list[self.current_answer]['status'] = "A"
            else:
                b['bg'] = 'red'
                b['activebackground'] = 'red'
                self.answer_btn['bg'] = 'green'
                self.answer_btn['activebackground'] = 'green'

                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    pass
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "R"
                elif status == "G":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                else:
                    self.controller.word_list[self.current_answer]['status'] = "R"

            self.controller.save_word_list()

            self.take_answer = False


class MeaningsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.bg_colour)
        self.__str__ = "MeaningsPage"

        ####### SETTINGS ########
        pad = controller.pad
        self.current_answer = ""
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.take_answer = True
        self.answer_btn = None
        self.answer_word = None

        ####### WIDGETS #######
        home_btn = Button(self, text="←", font=controller.big_font, bg=controller.button_colour,
                          relief="groove",
                          command=lambda: controller.show_frame("HomePage"))

        self.question_label = Label(self, text="", width=1, wraplength=412, bg=controller.bg_colour,
                                    font=controller.title_font)

        self.ans1_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans1_btn.configure(command=lambda btn=self.ans1_btn: self.submit_answer(btn))

        self.ans2_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans2_btn.configure(command=lambda btn=self.ans2_btn: self.submit_answer(btn))

        self.ans3_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans3_btn.configure(command=lambda btn=self.ans3_btn: self.submit_answer(btn))

        self.ans4_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans4_btn.configure(command=lambda btn=self.ans4_btn: self.submit_answer(btn))

        next_question = Button(self, text="Next", width=5, font=controller.big_font, bg=controller.button_colour,
                               relief="groove", command=self.next_word)

        ####### PLACEMENTS #######
        home_btn.place(x=pad, y=pad)
        self.question_label.grid(row=0, column=1, columnspan=6, sticky="nsew")
        self.ans1_btn.grid(row=1, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans2_btn.grid(row=1, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans3_btn.grid(row=2, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans4_btn.grid(row=2, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        next_question.place(x=482, y=93)

        ########## BINDS / PRESETS ########
        self.next_word()

    def next_word(self, e=0):
        sample_words = random.sample(list(self.controller.word_list.keys()), 4)
        self.answer_word = random.choice(sample_words)
        self.current_answer = self.controller.word_list[self.answer_word]['definition']
        self.question_label['text'] = self.answer_word
        self.ans1_btn['text'] = self.controller.word_list[sample_words[0]]['definition']
        self.ans2_btn['text'] = self.controller.word_list[sample_words[1]]['definition']
        self.ans3_btn['text'] = self.controller.word_list[sample_words[2]]['definition']
        self.ans4_btn['text'] = self.controller.word_list[sample_words[3]]['definition']

        for btn in (self.ans1_btn, self.ans2_btn, self.ans3_btn, self.ans4_btn):
            btn.configure(bg="white", activebackground="SystemButtonFace")
            if btn['text'] == self.current_answer:
                self.answer_btn = btn
        self.take_answer = True

    def submit_answer(self, b):
        if self.take_answer:
            ans = b['text']
            if ans == self.current_answer:
                b['bg'] = 'green'
                b['activebackground'] = 'green'
                status = self.controller.word_list[self.answer_word]['status']
                if status == "R":
                    self.controller.word_list[self.answer_word]['status'] = "A"
                elif status == "A":
                    self.controller.word_list[self.answer_word]['status'] = "G"
                elif status == "G":
                    pass
                else:
                    self.controller.word_list[self.answer_word]['status'] = "A"
            else:
                b['bg'] = 'red'
                b['activebackground'] = 'red'
                self.answer_btn['bg'] = 'green'
                self.answer_btn['activebackground'] = 'green'

                status = self.controller.word_list[self.answer_word]['status']
                if status == "R":
                    pass
                elif status == "A":
                    self.controller.word_list[self.answer_word]['status'] = "R"
                elif status == "G":
                    self.controller.word_list[self.answer_word]['status'] = "A"
                else:
                    self.controller.word_list[self.answer_word]['status'] = "R"

            self.controller.save_word_list()

            self.take_answer = False


class SpellingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.bg_colour)
        self.__str__ = "SpellingsPage"

        ####### SETTINGS ########
        pad = controller.pad
        self.current_answer = ""
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.take_answer = True
        self.answer_btn = None

        ####### WIDGETS #######
        home_btn = Button(self, text="←", font=controller.big_font, bg=controller.button_colour,
                          relief="groove",
                          command=lambda: controller.show_frame("HomePage"))

        self.question = st.ScrolledText(self, font=controller.big_font, bg=controller.button_colour, width=10,
                                             height=10, wrap="word", exportselection=False,
                                             relief="groove")

        self.answer = Text(self, font=controller.title_font, width=5, height=1, relief="solid")
        next_question = Button(self, text="Next", width=10, font=controller.big_font, bg=controller.button_colour,
                               relief="groove", command=self.next_word)

        ####### PLACEMENTS #######
        home_btn.place(x=pad, y=pad)
        self.question.grid(row=0, column=1, columnspan=6, padx=pad, pady=pad, sticky="nsew")
        self.answer.grid(row=1, column=1, columnspan=5, padx=pad, pady=pad, sticky="new" )
        next_question.grid(row=1, column=6, padx=pad, pady=pad, sticky='nwe')

        ########## BINDS / PRESETS ########
        self.answer.bind("<Return>", self.submit_answer)
        self.next_word()

    def next_word(self, e=0):
        self.current_answer = random.choice(list(self.controller.word_list.keys()))
        definition = self.controller.word_list[self.current_answer]['definition']
        korean_def = self.controller.word_list[self.current_answer]['korean']
        sentence = self.controller.word_list[self.current_answer]['example'].replace(
            self.current_answer, "_____")
        t = f"""
{definition}
        
{korean_def}

{sentence}

"""
        self.question.configure(state=NORMAL)
        self.question.delete(1.0, END)
        self.question.insert(INSERT, t, ("centered",))
        self.question.tag_configure("centered", justify="center")
        self.question.configure(state=DISABLED)

        self.answer.configure(state=NORMAL)
        self.answer.configure(fg='black')
        self.answer.delete(1.0, END)
        self.take_answer = True

    #TODO: here
    def submit_answer(self, e):
        if self.take_answer:
            ans = e.widget.get("1.0", "end-1c").lower()
            if ans == self.current_answer:
                self.answer.configure(fg='green')
                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "G"
                elif status == "G":
                    pass
                else:
                    self.controller.word_list[self.current_answer]['status'] = "A"
            else:
                self.answer.delete(1.0, END)
                self.answer.insert(END, self.current_answer)
                self.answer.configure(fg='red')

                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    pass
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "R"
                elif status == "G":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                else:
                    self.controller.word_list[self.current_answer]['status'] = "R"

            self.controller.save_word_list()

            self.answer.configure(state=DISABLED)
            self.take_answer = False

class SentencesPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.bg_colour)
        self.__str__ = "SentencesPage"

        ####### SETTINGS ########
        pad = controller.pad
        self.current_answer = ""
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.take_answer = True
        self.answer_btn = None

        ####### WIDGETS #######
        home_btn = Button(self, text="←", font=controller.big_font, bg=controller.button_colour,
                          relief="groove",
                          command=lambda: controller.show_frame("HomePage"))

        self.question_label = Label(self, text="", width=1, wraplength=412, bg=controller.bg_colour,
                                    font=controller.title_font)

        self.ans1_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans1_btn.configure(command=lambda btn=self.ans1_btn: self.submit_answer(btn))

        self.ans2_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans2_btn.configure(command=lambda btn=self.ans2_btn: self.submit_answer(btn))

        self.ans3_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans3_btn.configure(command=lambda btn=self.ans3_btn: self.submit_answer(btn))

        self.ans4_btn = Button(self, text="", width=1, font=controller.big_font, bg=controller.button_colour,
                               relief="groove")
        self.ans4_btn.configure(command=lambda btn=self.ans4_btn: self.submit_answer(btn))

        next_question = Button(self, text="Next", width=5, font=controller.big_font, bg=controller.button_colour,
                               relief="groove", command=self.next_word)

        ####### PLACEMENTS #######
        home_btn.place(x=pad, y=pad)
        self.question_label.grid(row=0, column=1, columnspan=6, sticky="nsew")
        self.ans1_btn.grid(row=1, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans2_btn.grid(row=1, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans3_btn.grid(row=2, column=0, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        self.ans4_btn.grid(row=2, column=4, columnspan=4, padx=pad, pady=pad, sticky="nsew")
        next_question.place(x=482, y=93)

        ########## BINDS / PRESETS ########
        self.next_word()

    def next_word(self, e=0):
        sample = random.sample(list(self.controller.word_list.keys()), 4)
        self.current_answer = random.choice(sample)
        self.question_label['text'] = self.controller.word_list[self.current_answer]['example'].replace(
            self.current_answer, "_____")
        self.ans1_btn['text'] = sample[0]
        self.ans2_btn['text'] = sample[1]
        self.ans3_btn['text'] = sample[2]
        self.ans4_btn['text'] = sample[3]

        for btn in (self.ans1_btn, self.ans2_btn, self.ans3_btn, self.ans4_btn):
            btn.configure(bg="white", activebackground="SystemButtonFace")
            if btn['text'] == self.current_answer:
                self.answer_btn = btn
        self.take_answer = True

    def submit_answer(self, b):
        if self.take_answer:
            ans = b['text']
            if ans == self.current_answer:
                b['bg'] = 'green'
                b['activebackground'] = 'green'
                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "G"
                elif status == "G":
                    pass
                else:
                    self.controller.word_list[self.current_answer]['status'] = "A"
            else:
                b['bg'] = 'red'
                b['activebackground'] = 'red'
                self.answer_btn['bg'] = 'green'
                self.answer_btn['activebackground'] = 'green'

                status = self.controller.word_list[self.current_answer]['status']
                if status == "R":
                    pass
                elif status == "A":
                    self.controller.word_list[self.current_answer]['status'] = "R"
                elif status == "G":
                    self.controller.word_list[self.current_answer]['status'] = "A"
                else:
                    self.controller.word_list[self.current_answer]['status'] = "R"

            self.controller.save_word_list()

            self.take_answer = False


class MutableText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


if __name__ == "__main__":
    app = App()
    app.mainloop()
