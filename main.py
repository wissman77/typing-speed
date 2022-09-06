from tkinter import Tk, Text, END
from tkinter import ttk
import random
import json


FONT = ('Arial', 16)
TEXT_FONT = ('Arial', 14)


def get_data():
    """ loading the typing tests from json file """
    with open('data.json') as f:
        data = json.load(f)
        phrases = [phrase['text'] for phrase in data]
    return phrases


def start_timer(event):
    """ global function starts when the user left click the textbox to start typing """
    global start_time
    if start_time == 0:
        # disable the textbox to prevent the user from typing and showing the results
        user_typing_text.config(state='disable')
        show_results()
    else:
        # format the time and keep call the function until minute finished
        time_display = ""
        start_time -= 1
        if start_time < 10:
            time_display = f'0{start_time} seconds'
        else:
            time_display = f'{start_time} seconds'
        timer_label.config(text=time_display)
        user_typing_text.after(1000, lambda : start_timer(event))


def show_results():
    """ calculating the results and showing them on the label """
    typing_words = typing_text.get('1.0', END).split()
    user_words = user_typing_text.get('1.0', END).split()
    correct = 0
    wrong = 0
    
    for index, word in enumerate(user_words):
        if word == typing_words[index]:
            correct +=1
        else:
            wrong += 1
    
    message = f'You have {wrong} wrong words and {correct} correct words, So your speed is {correct}/min'
    results_label.config(text=message)


def reset():
    """ Reset All controls and global start_time variable """
    global start_time, typing_blocks
    start_time = 60
    timer_label.config(text='When you ready start typing')
    random.shuffle(typing_blocks)
    typing_text.insert('1.0', typing_blocks[0])
    user_typing_text.config(state='normal')
    user_typing_text.delete('1.0', END)
    results_label.config(text='Results')


# number of seconds to start
start_time = 60
typing_blocks = get_data()


root = Tk()
root.title('Typing Speed Test')

frm = ttk.Frame(master=root, padding=10)
frm.grid()

timer_label = ttk.Label(frm, text='When you ready start typing', font=FONT)
timer_label.grid(row=0, column=0)

typing_text = Text(frm, width=80, height=6, wrap='word' ,font=TEXT_FONT, foreground='green')
random.shuffle(typing_blocks)
typing_text.insert('1.0', typing_blocks[0])
typing_text.config( state='disabled')
typing_text.grid(row=1, column=0)

ttk.Label(frm, text='Start typing here:', font=FONT).grid(row=2, column=0)

user_typing_text = Text(frm, width=80, height=6, wrap='word', font=TEXT_FONT)
user_typing_text.grid(row=3, column=0)
user_typing_text.bind('<Button-1>', start_timer)

results_label = ttk.Label(frm, text='Results', font=FONT, padding='10 10')
results_label.grid(row=4, column=0)

style = ttk.Style()
style.configure('my.TButton', font=FONT,padding='5 5')
reset_button = ttk.Button(frm, text='Reset', style='my.TButton', command=reset)
reset_button.grid(row=5, column=0)

root.mainloop()
