from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model import *
from data.neuro.local_models import *
from data.neuro.text_recognize_yolo import Text_Recognize_yolo
from data.result import Rama_prod


class Danila_rama_text_recognize_model_3(Danila_rama_text_recognize_model):
    def get_model(self, yolo_path):
        return Text_Recognize_yolo(model_path= LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_3, yolo_path=yolo_path)
    def get_prod_coefficients(self, rama_prod):
        if rama_prod == Rama_prod.Rama_Prod.altai:
            return Prod_coefficients(
                number_coefficients= Text_coefficients(
                    length= 5, height=160, width=160
                ),
                prod_coefficients= Text_coefficients(
                    length=4, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.balakovo:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=64, width=192
                ),
                prod_coefficients=Text_coefficients(
                    length=4, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.begickaya:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=6, height=160, width=160
                ),
                prod_coefficients=Text_coefficients(
                    length=2, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.promlit:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=96, width=96
                ),
                prod_coefficients=Text_coefficients(
                    length=2, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.ruzhimmash:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=192, width=192
                ),
                prod_coefficients=Text_coefficients(
                    length=4, height=128, width=128
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=96, width=96
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.tihvin:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=160, width=160
                ),
                prod_coefficients=Text_coefficients(
                    length=4, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif rama_prod == Rama_prod.Rama_Prod.uralvagon:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=64, width=160
                ),
                prod_coefficients=Text_coefficients(
                    length=1, height=128, width=128
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=128, width=128
                ),
            )