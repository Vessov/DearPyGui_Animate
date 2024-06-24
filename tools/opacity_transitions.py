
def precalculate_opacity(start:int,
                         end:int,
                         displacement:int,
                         bezier_factors:list) -> list[int]:
    """Precalculate list of every opacity that will be used during\
        the animation.

    Args:
        start (int): starting opacity as alfa value of RGBA notation
        end (int): ending opacity as alfa value of RGBA notation
        displacement (int): difference between starting and ending opacity
        bezier_factors (list): precalculated Bezier Factors for every step\
            between starting and ending opacities

    Returns:
        list[int]: grouping (list) of opacities for every step in the animation
    """
    
    # calculate delta of opacity between starting position
    # and every step based on bezier factors
    deltas = [displacement*factor for factor in bezier_factors]

    # calculate concrete opacities based on opacity deltas
    opacities = [int(start+delta) for delta in deltas]

    # assert that last calculated opacity is equal to end opacity
    # if not, change the last opacity to the end opacity
    try:
        assert opacities[-1] == end
    except AssertionError:
        opacities[-1] = end
    
    return opacities