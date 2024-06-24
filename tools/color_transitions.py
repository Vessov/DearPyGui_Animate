
def precalculate_colors(start:list|tuple,
                        end:list|tuple,
                        displacement:list,
                        bezier_factors:list) -> list[list[int]]:
    """Precalculate list of every color that will be used during the animation

    Args:
        start (list | tuple): starting color in RGB/RGBA values
        end (list | tuple): ending color in RGB/RGBA values
        displacement (list): difference between every starting and\
            ending RGB/RGBA value
        bezier_factors (list): precalculated Bezier Factors for every step\
            between starting and ending colors

    Returns:
        list[list[int]]: grouping (list) of RGB/RGBA values for every step\
            in the animation
    """
    
    # calculate delta of color between starting color
    # and every step based on bezier factors
    deltas = [[dis*factor for dis in displacement] # loops over every item in displacement
              for factor in bezier_factors]
    
    # calculate concrete colors based on color deltas
    colors = [[round(start[i]+delta[i]) for i in range(len(start))] # loops for every index in start[] and delta[]
              for delta in deltas]
    
    try:
        assert colors[-1] == end
    except AssertionError:
        colors[-1] = end

    return colors