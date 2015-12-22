from enum import Enum


class OrderConditions(Enum):
    Market = 0
    Limit = 1
    #Stop = 2
    #Conditional = 3
    #fill or kill? etc