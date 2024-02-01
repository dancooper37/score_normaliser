#!/user/bin/env python3

# ava.py

"""
Description: Tool to normalise archery scores between bowstyles and genders according to 2023 ArcheryGB handicap tables.
Author: Daniel Cooper (University of Liverpool Archery Club)
Date Created: 23/07/2023
Version: 0.1
Python Version: 3.10
Dependencies: numpy, pandas
License:
"""

# Focus is on indoors for now, ignoring difference between single and triple spot faces.

import pandas as pd
import math

hcaps = pd.read_csv("reverse_lookup_table.csv")


def get_raw(score, round):
    return hcaps.at[score, round]


def normalise(score, round, bowstyle, gender):
    raw = get_raw(score, round)
    adj = raw
    if bowstyle == "C":
        adj = raw + (raw * 0.1667) + 12.5
    elif bowstyle == "B":
        adj = raw + (raw * 0.2727) - 29.818
    elif bowstyle == "L":
        adj = raw + (raw * 0.1667) - 45.833
    if gender == "W":
        if bowstyle == "R":
            adj -= 5
        elif bowstyle == "C":
            adj -= 4
        elif bowstyle == "B":
            adj -= 5.5
        elif bowstyle == "L":
            adj -= 7
    return math.floor(adj)

def normalise_outdoor(score, round, bowstyle, gender):
    if bowstyle == "C":
        round += " Compound"
    raw = get_raw(score, round)
    adj = raw
    match bowstyle:
        case "C":
            adj = raw + (raw * 0.1667) + 12.5
        case "B":
            adj = raw + (raw * 0.2727) - 29.818
        case "L":
            adj = raw + (raw * 0.1667) - 45.833
        case _:
            pass
    match gender:
        case "W":
            match bowstyle:
                case "R":
                    adj -= 5
                case "C":
                    adj -= 4
                case "B":
                    adj -= 5.5
                case "L":
                    adj -= 7
    return math.floor(adj)

def normalise_indoor(score, round, bowstyle, gender):
    if bowstyle == "C":
        round += " Compound"
    raw = get_raw(score, round)
    adj = raw
    match bowstyle:
        case "C":
            adj = raw + (raw * 0.1667) + 12.5
        case "B":
            adj = raw + (raw * 0.2727) - 29.818
        case "L":
            adj = raw + (raw * 0.1667) - 45.833
        case _:
            pass
    match gender:
        case "W":
            match bowstyle:
                case "R":
                    adj -= 5
                case "C":
                    adj -= 4
                case "B":
                    adj -= 5.5
                case "L":
                    adj -= 7
    return math.floor(adj)

def get_equiv(handicap, round):
    if "Compound" in round:
        round = round.replace(" Compound", "")
    return min(hcaps[hcaps[round] == handicap].index.values)


# def load_ianseo():






"""
if "Compound" in round:
        return "n/a"
    else:"""


