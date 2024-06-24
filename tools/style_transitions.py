
def precalculate_styles(start:int|float,
                        end:int|float,
                        displacement:int|float,
                        bezier_factors:list) -> list[int|float]:
    
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