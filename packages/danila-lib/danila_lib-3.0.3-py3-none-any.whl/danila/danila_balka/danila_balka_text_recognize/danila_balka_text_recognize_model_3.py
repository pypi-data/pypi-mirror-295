from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_model import *
from data.neuro.balka_text_recognize_altai_yolo import Balka_Text_Recognize_altai_yolo
from data.neuro.balka_text_recognize_yolo import Balka_Text_Recognize_yolo
from data.neuro.local_models import *
from data.result.balka_prod import Balka_Prod


class Danila_balka_text_recognize_model_3(Danila_balka_text_recognize_model):
    def get_model(self, yolo_path):
        return Balka_Text_Recognize_yolo(model_path= LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_3, yolo_path=yolo_path)

    def get_model_altai(self, yolo_path):
        return Balka_Text_Recognize_altai_yolo(model_path=LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_3,
                                               yolo_path=yolo_path,
                                               prod_coefficients=self.get_altai_prod_coefficients())

    def get_prod_coefficients(self, balka_prod):

        if balka_prod == Balka_Prod.begickaya:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=64, width=64
                ),
                prod_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif balka_prod == Balka_Prod.promlit:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=192, width=192
                ),
                prod_coefficients=Text_coefficients(
                    length=2, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=32, width=32
                ),
            )
        elif balka_prod == Balka_Prod.ruzhimmash:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=128, width=128
                ),
                prod_coefficients=Text_coefficients(
                    length=4, height=96, width=96
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )
        elif balka_prod == Balka_Prod.tihvin:
            return Prod_coefficients(
                number_coefficients=Text_coefficients(
                    length=5, height=128, width=128
                ),
                prod_coefficients=Text_coefficients(
                    length=4, height=64, width=64
                ),
                year_coefficients=Text_coefficients(
                    length=2, height=64, width=64
                ),
            )

    def get_altai_prod_coefficients(self):

        return [
                Prod_coefficients(
                    number_coefficients=Text_coefficients(
                        length=5, height=96, width=96
                    ),
                    prod_coefficients=Text_coefficients(
                        length=4, height=96, width=96
                    ),
                    year_coefficients=Text_coefficients(
                        length=2, height=64, width=64
                    )
                ),
                Prod_coefficients(
                    number_coefficients=Text_coefficients(
                        length=6, height=192, width=192
                    ),
                    prod_coefficients=Text_coefficients(
                        length=4, height=96, width=96
                    ),
                    year_coefficients=Text_coefficients(
                        length=2, height=64, width=64
                    )
                )
            ]