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
    if gender == "W":
        if bowstyle == "R":
            adj -= 5
        elif bowstyle == "C":
            adj -= 4
        elif bowstyle == "B":
            adj -= 5.5
    return math.floor(adj)

normalise(1180, "York", "C", "W")




