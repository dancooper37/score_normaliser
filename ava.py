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


def normalise(score, round_name, bowstyle, gender, indoor_mode):
    if bowstyle == "C" and "Compound" not in round_name:
        round_name += " Compound"
    raw = get_raw(score, round_name)
    adj = raw
    if indoor_mode:
        match bowstyle:
            case "C":
                adj = raw + (raw * -0.0579) + 18.591
            case "B":
                adj = raw + (raw * 0.2065) - 19.807
            case "L":
                adj = raw + (raw * 0.1434) - 37.349
            case _:
                pass
        match gender:
            case 1:
                print("W")
                match bowstyle:
                    case "R":
                        adj -= 5
                    case "C":
                        adj -= 4
                    case "B":
                        adj -= 6
                    case "L":
                        adj -= 7
    else:
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
            case 1:
                print("W")
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
    handicap_list = []
    if "Compound" in round:
        round = round.replace(" Compound", "")
    try:
        handicap_list = min(hcaps[hcaps[round] == handicap].index.values)
    except ValueError:
        while not handicap_list:
            try:
                handicap += 1
                handicap_list = min(hcaps[hcaps[round] == handicap].index.values)
            except ValueError:
                continue
    return handicap_list
