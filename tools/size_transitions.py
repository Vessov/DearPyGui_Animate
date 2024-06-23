
def precalculate_sizes(start:list|tuple,
                       end:list|tuple,
                       displacement:list,
                       bezier_factors:list) -> list[list[int]]:
    
    # calculate delta of size between starting size
    # and every step based on bezier factors
    deltas = [[displacement[0]*factor, displacement[1]*factor]
              for factor in bezier_factors]
    
    # calculate concrete sizes based on size deltas
    sizes = [[round(start[0]+delta[0]),
              round(start[1]+delta[1])]
              for delta in deltas]
    
    # assert that the last calculated size is equal to end size
    # if not, change the last size to end size
    try:
        assert sizes[-1] == end
    except AssertionError:
        sizes[-1] = end
    
    return sizes