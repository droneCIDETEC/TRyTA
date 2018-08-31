from enum import Enum

class Fases(Enum):
    DISARMED = 0
    ARMING = 1
    TAKING_OFF = 2
    HOVERING = 3
    LINE_FOLLOWING = 4
    WINDOW_CROSSING = 5
    LOST = 6
    EMERGENCY = 7
    LANDING = 8
    DISARMING = 9
