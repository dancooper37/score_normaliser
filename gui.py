import tkinter
from tkinter import *
from tkinter import filedialog, ttk
from ttkthemes import ThemedTk

import pandas as pd

from ava import hcaps, normalise, normalise_outdoor, get_equiv

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
        hcap_norm = normalise_outdoor(score, round, bowstyle, gender)
        score_norm = get_equiv(hcap_norm, round)
        label_conv_hcap_dynamic.config(text=hcap_norm)
        label_equiv_dynamic.config(text=score_norm)
    elif "Local Bib" in bulk_import_file:
        bulk_import_file["norm_hcap"] = bulk_import_file.apply(
            lambda x: bulk_convert_hcap(x.Score, x.Division, x.Class, round), axis=1)
        print(bulk_import_file[["GivenName", "FamilyName", "Target", "Country", "Score", "norm_hcap"]].sort_values(
            "norm_hcap"))
    else:
        bulk_import_file["norm_hcap"] = bulk_import_file.apply(
            lambda x: bulk_convert_hcap(x.score, x.bowstyle, x.gender, round), axis=1)
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
    status_text = "Status: " + str(len(bulk_import_file)) + " Archers Found"
    label_status.configure(text=status_text)
    print(bulk_import_file[["WaID", "GivenName", "FamilyName", "Division", "Class", "Score"]])


window = ThemedTk(theme="plastik", background=True)
window.geometry("398x307+50+50")

label_score = ttk.Label(window, text="Score:")
label_score.place(x=10, y=10)

entry_score = ttk.Entry(window, width=13)
entry_score.place(x=105, y=10)

label_bowstyle = ttk.Label(window, text="Bowstyle:")
label_bowstyle.place(x=10, y=40)

bowstyle_options = ["R", "C", "B", "L"]
combo_bowstyle = ttk.Combobox(window, values=bowstyle_options, width=10, state="readonly")
combo_bowstyle.place(x=105, y=40)

label_gender = ttk.Label(window, text="Gender:")
label_gender.place(x=10, y=70)

gender_options = ["M", "W"]
combo_gender = ttk.Combobox(window, values=gender_options, width=10, state="readonly")
combo_gender.place(x=105, y=70)

separator = ttk.Separator(window, orient='horizontal')
separator.place(x=0, y=105, width=200)

all_rounds = tkinter.BooleanVar()
indoor = tkinter.BooleanVar()
outdoor = tkinter.BooleanVar()


def get_round_list(show_all, indoor_check, outdoor_check):
    rounds = []
    if indoor_check and not show_all:
        all_rounds = list(hcaps.columns.values)[9:]
        for round_name in all_rounds:
            if "Compound" not in round_name and "Triple" not in round_name:
                rounds.append(round_name)
                print(round_name)
    elif indoor_check and show_all:
        rounds = list(hcaps.columns.values)[9:]
    elif outdoor_check and not show_all:
        rounds = list(hcaps.columns.values)[0:9]
        rounds.remove("Score")
        for round_name in rounds:
            print(round_name)
            if "Compound" in round_name or "Triple" in round_name or "70m" in round_name:
                rounds.remove(round_name)
    elif outdoor_check and show_all:
        rounds = list(hcaps.columns.values)[0:9]
        rounds.remove("Score")
    return rounds


check_full_rounds = ttk.Checkbutton(window, text="Show All", variable=all_rounds)
check_full_rounds.place(x=120, y=115)

check_indoor = ttk.Checkbutton(window, text="Indoor", variable=indoor)
check_indoor.place(x=10, y=165)

check_outdoor = ttk.Checkbutton(window, text="Outdoor", variable=outdoor)
check_outdoor.place(x=70, y=165)

label_round = ttk.Label(window, text="Round:")
label_round.place(x=10, y=115)

round_options = get_round_list(all_rounds.get(), True, False)
combo_round = ttk.Combobox(window, values=round_options, width=26, state="readonly",
                           postcommand=lambda: combo_round.configure(values=get_round_list(all_rounds.get(), indoor.get(), outdoor.get())))
combo_round.place(x=10, y=135)


"""
label_compound_warn = ttk.Label(window,
                                text="N.B.: Indoor rounds with inner 10 ring scoring for compounds are listed separately.",
                                wraplength=200, justify=LEFT)
label_compound_warn.place(x=10, y=200)
"""

separator = ttk.Separator(window, orient='horizontal')
separator.place(x=0, y=195, width=200)

btn_convert = ttk.Button(window, text="Normalise This Score", width=28, command=get_params_csv)
btn_convert.place(x=10, y=272)

separator = ttk.Separator(window, orient='vertical')
separator.place(x=200, y=0, height=320)

label_conv_hcap_static = ttk.Label(window, text="RM Normalised Handicap:")
label_conv_hcap_static.place(x=10, y=210)

label_conv_hcap_dynamic = ttk.Label(window, text="0000")
label_conv_hcap_dynamic.place(x=160, y=210)

label_equiv_static = ttk.Label(window, text="Equivalent RM Score:")
label_equiv_static.place(x=10, y=240)

label_equiv_dynamic = ttk.Label(window, text="0000")
label_equiv_dynamic.place(x=160, y=240)

bulk_mode = tkinter.BooleanVar()

def enable_disable_bulk():
    btn_convert.configure(state=DISABLED if bulk_mode.get() else NORMAL)
    entry_score.configure(state=DISABLED if bulk_mode.get() else NORMAL)
    combo_gender.configure(state=DISABLED if bulk_mode.get() else NORMAL)
    combo_bowstyle.configure(state=DISABLED if bulk_mode.get() else NORMAL)
    button_import.configure(state=NORMAL if bulk_mode.get() else DISABLED)
    button_ianseo.configure(state=NORMAL if bulk_mode.get() else DISABLED)
    button_export.configure(state=NORMAL if bulk_mode.get() else DISABLED)

check_bulk_mode = ttk.Checkbutton(window, text="Enable Bulk Results Mode", variable=bulk_mode, command=enable_disable_bulk)
check_bulk_mode.place(x=210, y=10)

button_import = ttk.Button(window, text="Import from .csv", command=import_file, width=28, state=DISABLED)
button_import.place(x=210, y=40)

button_ianseo = ttk.Button(window, text="Import from IANSEO", command=import_ianseo, width=28, state=DISABLED)
button_ianseo.place(x=210, y=70)

label_status = ttk.Label(window, text="Status: No File Selected")
label_status.place(x=210, y=115)

button_export = ttk.Button(window, text="Export", width=28, state=DISABLED)
button_export.place(x=210, y=140)

separator = ttk.Separator(window, orient='horizontal')
separator.place(x=200, y=230, width=200)

button_settings = ttk.Button(window, text="Settings", width=28)
button_settings.place(x=210, y=242)

button_docs = ttk.Button(window, text="Documentation", width=28)
button_docs.place(x=210, y=272)

window.title("Archery Score Normaliser")
window.mainloop()
