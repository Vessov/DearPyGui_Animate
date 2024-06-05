
class BezierProgressUnderZero(Exception):
    def __init__(self, *args: object) -> None:
        message = "Time factor passed for Bezier progress calculation is smaller than zero!"
        super().__init__(message, *args)

class BezierProgressOverOne(Exception):
    def __init__(self, *args: object) -> None:
        message = "Time factor passed for Bezier progress calculation is bigger than one!"
        super().__init__(message, *args)
