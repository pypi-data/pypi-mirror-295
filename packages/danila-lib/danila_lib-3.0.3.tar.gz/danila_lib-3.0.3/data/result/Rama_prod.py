from enum import Enum


class Rama_Prod(Enum):
    altai = 0
    balakovo = 1
    begickaya = 2
    promlit = 3
    ruzhimmash = 4
    tihvin = 5
    uralvagon = 6
    no_rama = 7

class Rama_Prod_Conf:

    def __init__(self, rama_prod, conf):
        self.rama_prod = rama_prod
        self.conf = conf