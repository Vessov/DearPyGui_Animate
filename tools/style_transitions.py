
def precalculate_styles(start:int|float,
                        end:int|float,
                        displacement:int|float,
                        bezier_factors:list) -> list[int|float]:
    """Precalculate list of every style that will be used during the animation

    Attention:
        Currently any int or float above zero can be used as style start/end.\
            This is due to DearPyGUI allowing for various variables to be used\
            to define different styles (corner rounding, spacings, etc).\
            This is WIP and subject to change, as it will be in the future\
            restricted to the values supported by DearPyGUI for each style\
            variable.

    Args:
        start (int | float): starting style value
        end (int | float): ending style value
        displacement (int | float): difference between starting and\
            ending values
        bezier_factors (list): precalculated Bezier Factors for every step\
            between starting and ending styles

    Returns:
        list[int|float]: grouping (list) of concrete style values for every\
            step in the animation
    """
    
    # calculate delta of style between starting style
    # and every step based on bezier factors
    deltas = [displacement*factor for factor in bezier_factors]

    # calculate concrete styles based on style deltas
    # rounding to two places after comma
    styles = [round(start+delta, 2) for delta in deltas]

    # assert that last calculated style is equal to end style
    # if not, change the last style to end style
    try:
        assert styles[-1] == end
    except AssertionError:
        styles[-1] = end
    
    return styles