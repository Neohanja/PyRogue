# Random name generator for towns and NPCs
import random

class NameData:
    # Potential "prefixes" for towns and otherwise
    prefix = [
        "south",
        "north",
        "east",
        "west",
        "long",
        "short",
        "river",
        "pond",
        "lake",
        "ocean",
        "gold",
        "bronze",
        "silver",
        "farm",
        "black",
        "white",
        "red",
        "green",
        "orange",
        "blue",
        "smith",
        "crafter"
        ]
    suffix = [
        "town",
        "burg",
        "ton",
        "cove",
        "hovel",
        "burro",
        "villa",
        "pool",
        "hole",
        "stone",
        "shire",
        "bend",
        "ster",
        "mire"
    ]

def GenTownName(seed = ''):
    """ Using various lists, generates the name of a town """
    # Potential "prefixes" for a town name
    if seed == '':
        nRNG = random.Random()
    else:
        nRNG = random.Random(seed)

    pre = nRNG.random() < 0.25
    mid_count = nRNG.randint(0, 10)
    post = not pre or nRNG.random() < 0.35

    town_name = ''

    if pre:
        town_name += nRNG.choice(NameData.prefix)
        if nRNG.random() < .25:
            town_name += ' '
    if mid_count > 0:
        for i in range(mid_count):
            town_name += ChooseLetter(i % 2 == 1, nRNG.random())
    if post:
        if nRNG.random() < .25:
            town_name += ' '
        town_name += nRNG.choice(NameData.suffix)
    
    return town_name.title()

def GetCitizenName(l : int, nRNG : random.Random):
    """ Returns a name of (l) length"""
    name = ''
    while len(name) < l:
        name += ChooseLetter(nRNG.random() < 0.35, nRNG.random())
    return name

def ChooseLetter(vowel : bool, percent):
    if vowel:
        if percent <= 0.20:
            return 'a'
        elif percent <= 0.40:
            return 'e'
        elif percent <= 0.60:
            return 'i'
        elif percent <= 0.80:
            return 'o'
        else:
            return 'u'
    else:
        if percent <= 0.05:
            return 'b'
        elif percent <= 0.10:
            return 'c'
        elif percent <= 0.15:
            return 'd'
        elif percent <= 0.20:
            return 'f'
        elif percent <= 0.25:
            return 'g'
        elif percent <= 0.30:
            return 'h'
        elif percent <= 0.35:
            return 'j'
        elif percent <= 0.40:
            return 'k'
        elif percent <= 0.45:
            return 'l'
        elif percent <= 0.50:
            return 'm'
        elif percent <= 0.55:
            return 'n'
        elif percent <= 0.60:
            return 'p'
        elif percent <= 0.65:
            return 'qu'
        elif percent <= 0.70:
            return 'r'
        elif percent <= 0.75:
            return 's'
        elif percent <= 0.80:
            return 't'
        elif percent <= 0.85:
            return 'v'
        elif percent <= 0.90:
            return 'w'
        elif percent <= 0.95:
            return 'x'
        elif percent <= 0.97:
            return 'y'
        else:
            return 'z'