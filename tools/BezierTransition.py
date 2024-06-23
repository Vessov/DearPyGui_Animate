from src.standard_enums.PredefBezier import Bezier
import src.classes.Excepts as exc

def solve_bezier_transition(time:float,
                            bezier_handles:list|tuple|Bezier,
                            below_p0:bool=False,
                            over_p3:bool=False) -> float:
    """Solve Bezier curve progress using the Newton-Raphson method

    Args:
        time (float): Current time (x of the curve), as a factor of start to end;\
            example 12th frame out of 20 would be 12/20 = 0.6
        bezier_handles (list | tuple | Bezier): coordinates describing control\
            points P1 and P2 for Bezier curve, as [P1x, P1y, P2x, P2y]
        below_p0 (bool, optional): allow the progress calculation to return\
            values preceding P0 (`time` factor < 0). Defaults to False
        over_p3 (bool, optional): allow the progress calculation to return\
            values exceeding P3 (`time` factor > 1). Defaults to False

    Raises:
        exc.BezierProgressUnderZero: the `time` factor passed is lower than\
            zero, and the below_p0 flag restricts this calculation
        exc.BezierProgressOverOne: the `time` factor passed is bigger than\
            one, and the over_p3 flag restricts this calculation

    Returns:
        float: Progress of the curve (y) for the given time (x)
    """

    if isinstance(bezier_handles, Bezier):
        h1x, h1y, h2x, h2y = bezier_handles.value
    else:
        h1x, h1y, h2x, h2y = bezier_handles
    
    if time < 0 and below_p0 is False:
        raise exc.BezierProgressUnderZero()
    elif time > 1 and over_p3 is False:
        raise exc.BezierProgressOverOne()
    
    cx = 3 * h1x
    bx = 3 * (h2x - h1x) - cx
    ax = 1 - cx - bx

    t = time

    for _ in range(100):
        x = (ax * t ** 3 + bx * t ** 2 + cx * t) - time

        if round(x, 4) == 0:
            break

        dx = 3.0 * ax * t ** 2 + 2.0 * bx * t + cx

        t -= (x / dx)
    
    return 3 * t * (1 - t) ** 2 * h1y + 3 * t ** 2 * (1 - t) * h2y + t ** 3


def precalculate_bezier_factors(start:int,
                                last:int,
                                bezier_handles:list|tuple|Bezier) -> list[float]:
    
    """Precalculate all Bezier factors for given starting and ending positions

    Calculate progress (y) of Bezier curve for each point of time (x) between
    `start` and `last` and format them into a list, which can be used as factor
    for calculating next positions.

    Args:
        start (int): starting point in time (for example a frame when animation\
            will start). Should be non-negative and smaller than `last`.
        last (int): last point in time (for example a frame when animation\
            will end). Should be non-negative and bigger than `start`.
        bezier_handles (list | tuple | Bezier): coordinates describing control\
            points P1 and P2 for Bezier curve, as [P1x, P1y, P2x, P2y]

    Returns:
        list (float): list of Bezier curve progressions (y) for each point in time between `start` and `last`
    """

    factors = []
    for i in range(start, last+1):
        inter_result = solve_bezier_transition(i/last, bezier_handles)
        factors.append(inter_result)

    return factors

    # list comprehension (below) tested with timeit(); no real speed gained
    # therfore, the actual verbose code left as-is, for readability reasons
    #
    # return [solve_bezier_transition(i/last, bezier_handles) for i in range(start, last+1)]
