# Handles color manipulation based on
# strings and a dictionary. Some colors
# will have "special" effects, such as
# cycling through a spectrum of colors


COLOR_PALLET = {
    "White" : [255, 255, 255],
    "Black" : [0, 0, 0],
    "Blue" : [25, 65, 155],
    "Brown" : [125, 42, 42],
    "Green" : [86, 150, 70],
    "Tristian" : [200, 160, 160],
    "Olive" : [85, 71, 14],
    "Tan" : [247, 220, 180],
    "Grey" : [125, 125, 125],
    "Dark Grey" : [75, 75, 75],
    "Portal" : [71, 204, 231]
    }

def GetColor(color_name : str):
    """ Returns the rgb of a named color """
    # A friendly reminder, mostly I either spelled something wrong, used a
    # placeholder color, or forgot to change the name of something (like a previous 'Rainbow')
    if color_name not in COLOR_PALLET:
        print(color_name, 'does not exist. Remember to build it later.')
        COLOR_PALLET[color_name] = [255, 0, 255]

    # Sepcial Colors
    # We will not be using special colors for now, as this is not in the scope of what
    # **needs** to be done before completion. In further updates, this may be added.

    # Base Colors
    return COLOR_PALLET[color_name]