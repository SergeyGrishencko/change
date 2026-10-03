from enum import Enum


class GoalStatusEnum(str, Enum):
    active = 'Active'
    completed = 'Completed'
    on_hold = 'On Hold'
    canceled = 'Canceled' 