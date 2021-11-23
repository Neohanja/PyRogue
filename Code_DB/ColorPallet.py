# Handles color manipulation based on
# strings and a dictionary. Some colors
# will have "special" effects, such as
# cycling through a spectrum of colors
import MathFun

COLOR_PALLET = {
    "White" : [255, 255, 255],
    "Black" : [0, 0, 0],
    "Blue" : [25, 65, 155],
    "Light Blue" : [55, 125, 200],
    "Brown" : [125, 42, 42],
    "Green" : [86, 150, 70],
    "Tristian" : [200, 160, 160],
    "Olive" : [85, 71, 14],
    "Tan" : [247, 220, 180],
    "Light Grey" : [175, 175, 175],
    "Grey" : [125, 125, 125],
    "Dark Grey" : [75, 75, 75],
    "Portal" : [71, 204, 231],
    "Orange" : [255, 133, 51],
    "Bloody" : [175, 0, 50]
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

def ColorLerp(a_color : str, b_color : str, blend_percent : float):
    """ 
        Lerps between two colors in a library. 
        Clamps percent between 0 and 1.
        Also ensures A and B are in the color pallet, or 
        adds it as a Magenta placeholder.
    """
    blend_percent = MathFun.Clamp(0.0, 1.0, blend_percent)
    a = GetColor(a_color)
    b = GetColor(b_color)
    col = []
    for rgb in range(3):
        col += [MathFun.Floor(MathFun.Lerp(b[rgb], a[rgb], blend_percent))]
    return col