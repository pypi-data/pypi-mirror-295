import abc

class Prod_coefficients:
    def __init__(self, number_coefficients, prod_coefficients, year_coefficients):
        self.number_coefficients = number_coefficients
        self.prod_coefficients = prod_coefficients
        self.year_coefficients = year_coefficients

class Text_coefficients:
    def __init__(self, length, height, width):
        self.length = length
        self.height = height
        self.width = width

class Danila_balka_text_recognize_model(abc.ABC):
    @abc.abstractmethod
    def get_model(self, yolo_path): pass

    @abc.abstractmethod
    def get_prod_coefficients(self, balka_prod): pass

    @abc.abstractmethod
    def get_model_altai(self, yolo_path): pass

    @abc.abstractmethod
    def get_altai_prod_coefficients(self): pass
