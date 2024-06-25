from dataclasses import dataclass
import uuid

from src.classes.Animation import Animation


@dataclass
class ObjectAnimations:
    """Class that gathers all animations enacted on specific object.

    Collects all registered animations of every type in a dictionaries\
    for efficient access, and lists ID's of currently active animations of\
    every type to be animated

    Attributes:
        animated_object (str | int): the reference to ID of the animated\
            object. Generally, the DearPyGUI tag associated with the object
        active_color_animations (list[uuid.UUID]): all currently played\
            color animations
        all_color_animations (dict[Animation]): all color animation objects\
            associated with the animated object
        active_opacity_animations (list[uuid.UUID]): all currently played\
            opacity animations
        all_opacity_animations (dict[Animation]):  all opacity animation\
            objects associated with the animated object
        active_position_animations (list[uuid.UUID]): all currently played\
            position animations
        all_position_animations (dict[Animation]):  all position animation\
            objects associated with the animated object
        active_size_animations (list[uuid.UUID]): all currently played\
            size animations
        all_size_animations (dict[Animation]):  all size animation objects\
            associated with the animated object
        active_style_animations (list[uuid.UUID]): all currently played\
            style animations
        all_style_animations (dict[Animation]):  all style animation objects\
            associated with the animated object

    """
    animated_object:str|int
    active_color_animations: list[uuid.UUID]
    all_color_animations: dict[Animation]
    active_opacity_animations: list[uuid.UUID]
    all_opacity_animations: dict[Animation]
    active_position_animations: list[uuid.UUID]
    all_position_animations: dict[Animation]
    active_size_animations: list[uuid.UUID]
    all_size_animations: dict[Animation]
    active_style_animations: list[uuid.UUID]
    all_style_animations: dict[Animation]
