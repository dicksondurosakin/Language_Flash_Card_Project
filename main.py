import pandas
from tkinter import *
import random

# Here i set some starting variables because i had many local scope that i used globally
english_word = None
spanish_word = None
familiar_a = None
familiar_b = None
comp_choice = None
learn_list = None
spanish_list = None
time_w = 0

BACKGROUND = "#B1DDC6"


# This function shows the back of the card, delete the topmost text,
# changes spanish to english and shows the english meaning
def show_back():
    global english_word, familiar_b, familiar_a
    canvas.itemconfig(front_canvas, image=back_image, )
    canvas.grid(row=0, column=1)
    canvas.itemconfig(first_text, text="English")
    canvas.itemconfig(second_text, text=f"{english_word}")
    canvas.delete(familiar_a,)
    canvas.delete( familiar_b)
    familiar_b = canvas.create_text(400, 50, text="Did you get it correctly? ", font=16)


# This function draws words from the words to learn deck which has already been filtered
# to include only words that you do not know. Then it display the spanish word you want to learn
def words_to_learn():
    global english_word, spanish_word, first_text, second_text, familiar_a, familiar_b, comp_choice, learn_list
    word_to_learn_csv = pandas.read_csv("word_to_learn.csv")
    learn_list = [{"spanish": value.spanish, "english": value.english} for (index, value) in
                  word_to_learn_csv.iterrows()]
    comp_choice = random.randint(0, len(word_to_learn_csv) - 1)
    spanish_word = learn_list[comp_choice]["spanish"]
    english_word = learn_list[comp_choice]["english"]
    canvas.delete(second_text, familiar_b)
    canvas.itemconfig(front_canvas, image=front_image, )
    canvas.grid(row=0, column=1)
    canvas.delete(second_text, familiar_b, familiar_a)
    canvas.itemconfig(first_text, text="Spanish")
    second_text = canvas.create_text(400, 280, text=spanish_word, font=("arial", 50, "bold"))
    familiar_a = canvas.create_text(400, 50, text="Do you know the English meaning of this word? ", font=16)


# This function creates the words to learn deck from the spanish word deck
# since it originally doesnt start with the code
def file_not_found():
    global spanish_list, comp_choice, spanish_word, english_word
    spanish_csv = pandas.read_csv("spanish_words.csv")
    spanish_list = [{"spanish": value.word, "english": value.meaning} for (index, value) in spanish_csv.iterrows()]
    comp_choice = random.randint(0, len(spanish_csv) - 1)
    spanish_word = spanish_list[comp_choice]["spanish"]
    english_word = spanish_list[comp_choice]["english"]
    spanish_dataframe = pandas.DataFrame(spanish_list)
    spanish_dataframe.to_csv("word_to_learn.csv")


# This function keeps all the words in the words to learn deck because you don't know them yet
def i_dont_know_this_word():
    global time_w

    try:
        words_to_learn()
    except FileNotFoundError:
        file_not_found()
    if time_w == 0:
        pass
    else:
        window.after_cancel(time_w)
    time_w = window.after(3000, show_back)


# This function delete a word from the word to learn deck since you already know them
def i_know_the_word():
    global english_word, spanish_word, first_text, second_text, familiar_a, familiar_b, comp_choice, learn_list, time_w

    try:
        if comp_choice == None:
            pass
        else:
            learn_list.pop(comp_choice)
            learn_dataframe = pandas.DataFrame(learn_list)
            learn_dataframe.to_csv("word_to_learn.csv")
        word_to_learn_csv = pandas.read_csv("word_to_learn.csv")
        learn_list = [{"spanish": value.spanish, "english": value.english} for (index, value) in
                      word_to_learn_csv.iterrows()]
        if len(word_to_learn_csv) <= 3:
            file_not_found()
            words_to_learn()
        comp_choice = random.randint(0, len(word_to_learn_csv) - 1)
        spanish_word = learn_list[comp_choice]["spanish"]
        english_word = learn_list[comp_choice]["english"]
        learn_dataframe = pandas.DataFrame(learn_list)
        learn_dataframe.to_csv("word_to_learn.csv")

    except FileNotFoundError:
        file_not_found()
        words_to_learn()
    finally:
        canvas.delete(second_text, familiar_b)
        canvas.itemconfig(front_canvas, image=front_image)
        canvas.grid(row=0, column=1)
        canvas.delete(second_text, familiar_b, familiar_a)
        canvas.itemconfig(first_text, text="Spanish")
        second_text = canvas.create_text(400, 280, text=spanish_word, font=("arial", 50, "bold"))
        familiar_a = canvas.create_text(400, 50, text="Do you know the English meaning of this word? ", font=16)

    if time_w == 0:
        pass
    else:
        window.after_cancel(time_w)
    time_w = window.after(3000, show_back)


# ------------------------------------- UI SETUP-------------------------------------
window = Tk()
window.title("Flash Card Project")
window.minsize(width=800, height=680, )
window.config(padx=20, pady=20, bg=BACKGROUND, )

canvas = Canvas(width=800, height=526, bg=BACKGROUND, highlightthickness=0)
front_image = PhotoImage(file="../Language_Flash_Card_Project/images/card_front.png")
back_image = PhotoImage(file="../Language_Flash_Card_Project/images/card_back.png")
front_canvas = canvas.create_image(410, 263, image=front_image,)
first_text = canvas.create_text(400, 150, text=f"Spanish", font=("arial", 30, "normal"))
second_text = canvas.create_text(400, 280, text=f"Word", font=("arial", 50, "bold"))
canvas.grid(row=0, column=1, columnspan=2)


wrong_image = PhotoImage(file="../Language_Flash_Card_Project/images/wrong.png")
wrong_button = Button(image=wrong_image, command=i_dont_know_this_word, highlightthickness=0)
wrong_button.grid(row=1, column=1)

right_image = PhotoImage(file="../Language_Flash_Card_Project/images/right.png")
right_button = Button(image=right_image, command=i_know_the_word, highlightthickness=0)
right_button.grid(row=1, column=2)
window.mainloop()
