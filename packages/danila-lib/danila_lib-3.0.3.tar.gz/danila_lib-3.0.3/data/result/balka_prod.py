from enum import Enum


class Balka_Prod(Enum):
    altai = 0
    begickaya = 1
    promlit = 2
    ruzhimmash = 3
    tihvin = 4
    no_balka = 5

class Balka_Prod_Conf:

    def __init__(self, balka_prod, conf):
        self.balka_prod = balka_prod
        self.conf = conf