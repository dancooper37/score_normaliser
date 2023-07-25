from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Separator

import pandas as pd

from ava import hcaps, normalise, get_equiv

bulk_import_file = pd.DataFrame()

def bulk_convert_hcap(score, bowstyle, gender, round):
    if bowstyle == "C":
        round += " Compound"
    norm_hcap = normalise(score, round, bowstyle, gender)
    return norm_hcap

def get_params_csv():
    round = combo_round.get()
    if bulk_import_file.empty:
        score = int(entry_score.get())
        bowstyle = combo_bowstyle.get()
        gender = combo_gender.get()
        hcap_norm = normalise(score, round, bowstyle, gender)
        score_norm = get_equiv(hcap_norm, round)
        label_conv_hcap_dynamic.config(text=hcap_norm)
        label_equiv_dynamic.config(text=score_norm)
    elif "Local Bib" in bulk_import_file:
        bulk_import_file["norm_hcap"] = bulk_import_file.apply(lambda x: bulk_convert_hcap(x.Score, x.Division, x.Class, round), axis=1)
        print(bulk_import_file[["GivenName", "FamilyName", "Target", "Country", "Score", "norm_hcap"]].sort_values("norm_hcap"))
    else:
        bulk_import_file["norm_hcap"] = bulk_import_file.apply(lambda x: bulk_convert_hcap(x.score, x.bowstyle, x.gender, round), axis=1)
        print(bulk_import_file)


def import_file():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select File",
                                          filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    global bulk_import_file
    bulk_import_file = pd.read_csv(filename)

def import_ianseo():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select File",
                                          filetypes=(("TXT Files", "*.txt"), ("All Files", "*.*")))
    global bulk_import_file
    bulk_import_file = pd.read_csv(filename, delimiter=";")




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

btn_convert = Button(window, text="Convert", width=24, height=3, command=get_params_csv)
btn_convert.place(x=10, y=232)

separator = Separator(window, orient='vertical')
separator.place(x=200, y=0, height=300)

label_conv_hcap_static = Label(window, text="Normalised Handicap:")
label_conv_hcap_static.place(x=210, y=10)

label_conv_hcap_dynamic = Label(window, text="0000")
label_conv_hcap_dynamic.place(x=350, y=10)

label_equiv_static = Label(window, text="Equiv. RM Score:")
label_equiv_static.place(x=210, y=40)

label_equiv_dynamic = Label(window, text="0000")
label_equiv_dynamic.place(x=350, y=40)

button_import = Button(window, text="Import .csv", command=import_file)
button_import.place(x=210, y=70)

button_ianseo = Button(window, text="Import IANSEO Results File", command=import_ianseo)
button_ianseo.place(x=210, y=100)

window.title("Archery Score Normaliser")
window.mainloop()
