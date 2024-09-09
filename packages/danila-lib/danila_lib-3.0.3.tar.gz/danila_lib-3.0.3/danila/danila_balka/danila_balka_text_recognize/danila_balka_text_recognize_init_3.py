from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_altai_work import \
    Danila_balka_text_recognize_altai_work
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_model_3 import \
    Danila_balka_text_recognize_model_3
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_work import \
    Danila_balka_text_recognize_work
from data.result.balka_prod import Balka_Prod


class Danila_balka_text_recognize_init_3:
    def __init__(self, yolov5_dir):
        danila_balka_text_recognize_model = Danila_balka_text_recognize_model_3()
        model = danila_balka_text_recognize_model.get_model(yolov5_dir)
        model_altai = danila_balka_text_recognize_model.get_model_altai(yolov5_dir)
        self.prod_models = {}
        for balka_prod in Balka_Prod:
            if balka_prod == Balka_Prod.altai:
                self.prod_models[balka_prod] = Danila_balka_text_recognize_altai_work(
                    text_recognize_model=model_altai
                )
            else:
                self.prod_models[balka_prod] = Danila_balka_text_recognize_work(
                    text_recognize_model=model,
                    prod_coefficients=danila_balka_text_recognize_model.get_prod_coefficients(balka_prod)
                )

    def balka_text_recognize(self, balka_prod, img_cut, image_text_areas):
        return self.prod_models[balka_prod].balka_text_recognize(balka_prod, img_cut, image_text_areas)

