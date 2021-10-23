# Handles color manipulation based on
# strings and a dictionary. Some colors
# will have "special" effects, such as
# cycling through a spectrum of colors

class ColorLibrary:
    """ 
        Meant to be a static class, there 
        should be no full instance made of
        this class and most things should be
        references from the functions described.
        That being said, a non-static instance
        will be made for time based items, such
        as portal timing and other entities
    """
    color_pallet = {
        "White" : [255, 255, 255],
        "Black" : [0, 0, 0],
        "Blue" : [25, 65, 155],
        "Brown" : [125, 42, 42],
        "Green" : [86, 150, 70],
        "Tristian" : [200, 160, 160],
        "Olive" : [85, 71, 14],
        "Tan" : [247, 220, 180],
        "Grey" : [125, 125, 125],
        "Dark Grey" : [75, 75, 75]
    }

    def GetColor(color_name : str):
        """ Returns the rgb of a named color """
        if color_name not in ColorLibrary.color_pallet:
            print(color_name, 'does not exist. Remember to build it later.')
            return [255, 0, 255] # Default color, an annoying magenta that is used for alpha range typically
        return ColorLibrary.color_pallet[color_name]