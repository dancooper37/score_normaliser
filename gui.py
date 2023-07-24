from tkinter import *
from tkinter.ttk import Combobox, Separator

from ava import hcaps, normalise

def get_params():
    score = int(entry_score.get())
    bowstyle = combo_bowstyle.get()
    gender = combo_gender.get()
    round = combo_round.get()
    label_conv_hcap_dynamic.config(text=normalise(score, round, bowstyle, gender))

window = Tk()
window.geometry("400x300+50+50")

label_score = Label(window, text="Score:")
label_score.place(x=10, y=10)

entry_score = Entry(window, width=13)
entry_score.place(x=105, y=10)

label_bowstyle = Label(window, text="Bowstyle:")
label_bowstyle.place(x=10, y=40)

bowstyle_options = ["R", "C", "B"]
combo_bowstyle = Combobox(window, values=bowstyle_options, width=10)
combo_bowstyle.place(x=105, y=40)

label_gender = Label(window, text="Gender:")
label_gender.place(x=10, y=70)

gender_options = ["M", "W"]
combo_gender = Combobox(window, values=gender_options, width=10)
combo_gender.place(x=105, y=70)

separator = Separator(window, orient='horizontal')
separator.place(x=0, y=105, width=200)

label_round = Label(window, text="Round:")
label_round.place(x=10, y=115)

round_options = list(hcaps.columns.values)
round_options.remove("Score")
combo_round = Combobox(window, values=round_options, width=26)
combo_round.place(x=10, y=135)

label_compound_warn = Label(window, text="N.B.: Indoor rounds with inner 10 ring scoring for compounds are listed separately.",
                            wraplength=200, justify=LEFT)
label_compound_warn.place(x=10, y=160)

separator = Separator(window, orient='horizontal')
separator.place(x=0, y=220, width=200)

btn_convert = Button(window, text="Convert", width=24, height=3, command=get_params)
btn_convert.place(x=10, y=232)

separator = Separator(window, orient='vertical')
separator.place(x=200, y=0, height=300)

label_conv_hcap_static = Label(window, text="Normalised Handicap:")
label_conv_hcap_static.place(x=210, y=10)

label_conv_hcap_dynamic = Label(window, text="0000")
label_conv_hcap_dynamic.place(x=350, y=10)

label_equiv_static = Label(window, text="Equiv. RM Score:")
label_equiv_static.place(x=210, y=40)

label_equiv_dynamic = Label(window, text="null")
label_equiv_dynamic.place(x=350, y=40)

window.title("Archery Score Normaliser")
window.mainloop()
