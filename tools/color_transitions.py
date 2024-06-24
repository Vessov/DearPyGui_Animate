
def precalculate_colors(start:list|tuple,
                        end:list|tuple,
                        displacement:list,
                        bezier_factors:list) -> list[list[int]]:
    
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