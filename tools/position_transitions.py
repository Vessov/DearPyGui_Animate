
def precalculate_positions(start:list|tuple,
                           end:list|tuple,
                           displacement:list,
                           bezier_factors:list) -> list[list[int]]:

    # calculate delta of movement between starting position
    # and every step based on bezier factors
    deltas = [[displacement[0]*factor, displacement[1]*factor] 
              for factor in bezier_factors]
    
    # calculate concrete positions based on movement deltas
    positions = [[round(start[0]+delta[0]),
                  round(start[1]+delta[1])]
                  for delta in deltas]
    
    # assert that the last calculated position is equal to end position
    # if not, change the last position to end position
    try:
        assert positions[-1] == end
    except AssertionError:
        positions[-1] = end

    return positions

def get_all_movements():
    pass

def calculate_full_movement():
    pass
