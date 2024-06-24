import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

import dearpygui.dearpygui as dpg

from src.standard_enums.AnimationTypes import AnimationType
from src.standard_enums.LoopTypes import Loops
from src.standard_enums.PredefBezier import Bezier
from tools.BezierTransition import precalculate_bezier_factors
from tools.color_transitions import precalculate_colors
from tools.opacity_transitions import precalculate_opacity
from tools.position_transitions import precalculate_positions
from tools.size_transitions import precalculate_sizes
from tools.style_transitions import precalculate_styles


def calc_dislpacement(start:int|float|list,
                      end:int|float|list) -> int|list:
    """Calculate displacement - difference between starting and ending steps.

    Args:
        start (int|float|list): beginning step (start position, opacity, etc)
        end (int|float|list): final step (end position, opacity, etc)

    Raises:
        ValueError: `start` and `end` args are of different types or lengths

    Returns:
        int|list: concrete displacement (or list of displacements) between\
            start and end
    """
    
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        return end - start
    
    elif (isinstance(start, list) and isinstance(end, list) 
          and len(start) == len(end)):
        return [end_n - start_n for start_n, end_n in zip(start, end)]

    else:
        raise ValueError("Both start and end has to be the same type and length")

def normalize_value(value:int|float|list,
                    animation_type:AnimationType,
                    animated_object:int|str) -> int|float|list:
    """Normalize values depending on the type of animation in which they'll\
        be used.

    Args:
        value (int|float|list): value to be normalized
        animation_type (AnimationType): type of animation in which the `value`\
            will be used
        animated_object (int|str): DearPyGUI tag of the object which will be\
            animated

    Returns:
        int|float|list: normalized value
    """
    
    obj = dpg.get_item_type(animated_object)
    normalized_value:list

    match animation_type:
        case AnimationType.SIZE:
            if obj == "mvAppItemType::mvWindowAppItem":
                normalized_value = [max(32, int(v)) for v in value]
            else:
                normalized_value = [max(1, int(v)) for v in value]
    
        case AnimationType.COLOR:
            normalized_value = [max(0, min(int(element), 255)) for element in value]
    
        case AnimationType.OPACITY:
            normalized_value = max(0, min(int(value), 255))

        case AnimationType.STYLE:
            normalized_value = value if value > 0 else 0

        case _:
            normalized_value = [int(v) for v in value]
    
    return normalized_value

def precalculate_step_values(animation_type:AnimationType,
                             start:int|float|list,
                             end:int|float|list,
                             displacement:int|float|list,
                             bezier_factors:list) -> list:
    """Precalculate concrete steps to avoid slowdowns and unnecessary\
            overheads during the running of the GUI.

    Args:
        animation_type (AnimationType): type of the animation that will be\
            played
        start (int | float | list): starting step of the animation (position,\
            size, opacity, etc)
        end (int | float | list): ending step of the animation (position, size,\
            opacity, etc.)
        displacement (int | float | list): the displacement (difference)\
            between the `start` and `end`
        bezier_factors (list): precalculated factors by which every step should\
            be multiplied to achieve correct Bezier progression of animation

    Returns:
        list: precalculated concrete values of steps to be animated
    """
    
    match animation_type:

        case AnimationType.POSITION:
            return precalculate_positions(start, end, displacement,
                                          bezier_factors)
        
        case AnimationType.OPACITY:
            return precalculate_opacity(start, end, displacement,
                                        bezier_factors)
        
        case AnimationType.SIZE:
            return precalculate_sizes(start, end, displacement,
                                      bezier_factors)

        case AnimationType.COLOR:
            return precalculate_colors(start, end, displacement,
                                       bezier_factors)
        
        case AnimationType.STYLE:
            return precalculate_styles(start, end, displacement,
                                       bezier_factors)


@dataclass
class Animation:
    """Class representing a single animation to be enacted on specified object

    Attributes:
        animation_type (AnimationType): type of animation to be created
        animated_object (int|str): reference to DearPyGUI tag of the object\
            which is going to be animated
        starting_value (int|float|list|tuple): beginning value of the objects\
            attribute (for example size, color, etc) from which the animation\
            should start
        ending_value (int|float|list|tuple): ending value of the objects\
            attribute (for example size, color, etc) on which the animation\
            should end
        bezier_handles (list|tuple|Bezier): Bezier curve handle points to be\
            used in the animation progression, in the format\
            of [P1x, P1y, P2x, P2y]
        duration (int): number of frames for which the animation should run
        start_frame (int, optional): the frame on which the animation should\
            start. Defaults to 0. Higher values will postpone animation\
            beginning by defined number of frames after the animation\
            start call was made
        animation_id (uuid.UUID, optional): the ID of the animation, which can\
            be used to get the reference to the animation object, or to pass\
            the reference to any DearPyGUI_Animate function
        loop_type (Loops|None, optional): type of loop in which the animation\
            should play
        start_callback (Callable|None, optional): callback function that will\
            be run at the start of the animation
        start_callback_data (Any|None, optional): data to be passed to the\
            `start_callback` function
        end_callback (Callable|None, optional): callback function that will be\
            run at the end of the animation
        end_callback_data (Any|None, optional): data to be passed to the\
            `end_callback` function
    """
    animation_type: AnimationType
    animated_object: int|str
    starting_value: int|float|list|tuple
    ending_value: int|float|list|tuple
    bezier_handles: list|tuple|Bezier
    duration: int
    start_frame: int = 0
    animation_id: uuid.UUID = field(default_factory=uuid.uuid4)
    loop_type: Loops|None = None
    start_callback: Callable|None = None
    start_callback_data: Any|None = None
    end_callback: Callable|None = None
    end_callback_data: Any|None = None

    def __post_init__(self) -> None:

        self._frame_counter:int = 0  # number of frame on which the animation is currently at
        self._loop_counter:int = 0  # iteration of loop on which the animation is currently at
        self._isplaying:bool = False
        self._ispaused:bool = False
        self._isreversed:bool = False
        self._end_frame:int = self.start_frame + self.duration  # on which frame the animation should end (relative to `start_frame`)
        
        
        # normalizing functions
        self.starting_value = normalize_value(self.starting_value,
                                              self.animation_type,
                                              self.animated_object)
        self.ending_value = normalize_value(self.ending_value,
                                            self.animation_type,
                                            self.animated_object)
        
        # calculate displacement after normalization
        self._displacement:int|list = calc_dislpacement(self.starting_value,
                                                       self.ending_value)
        
        # precalculations
        self._bezier_factors = precalculate_bezier_factors(start=self.start_frame,
                                                          last=self._end_frame,
                                                          bezier_handles=self.bezier_handles)
        
        self._step_values = precalculate_step_values(self.animation_type,
                                                    self.starting_value,
                                                    self.ending_value,
                                                    self._displacement,
                                                    self._bezier_factors)
