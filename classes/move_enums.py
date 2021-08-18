from enum import Enum

class MoveDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8


class MoveAbility(Enum):
    CAN_MOVE = 1
    CAN_CAPTURE = 2
    BLOCKED = 3
