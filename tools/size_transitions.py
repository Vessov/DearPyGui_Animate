
def precalculate_sizes(start:list|tuple,
                       end:list|tuple,
                       displacement:list,
                       bezier_factors:list) -> list[list[int]]:
    """Precalculate list of every size that will be used during the animation.

    Important:
        Every size is described as [X, Y] sizes of the item. Due to DearPyGUI\
            constraints, no item's size (either X or Y) can be smaller than 1,\
            and no windows size (either X or Y) can be smaller than 32

    Args:
        start (list | tuple): starting size as [X, Y] size
        end (list | tuple): ending size as [X, Y] size
        displacement (list): difference between every dimension size in\
            starting and ending sizes
        bezier_factors (list): precalculated Bezier Factors for every step\
            between starting and ending sizes

    Returns:
        list[list[int]]: group (list) of [X, Y] sizes for every step\
            in the animation
    """
    
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