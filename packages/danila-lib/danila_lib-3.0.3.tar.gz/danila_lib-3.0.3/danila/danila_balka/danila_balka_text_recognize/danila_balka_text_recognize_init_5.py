from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_altai_work import \
    Danila_balka_text_recognize_altai_work
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_model_3 import \
    Danila_balka_text_recognize_model_3
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_model_4 import \
    Danila_balka_text_recognize_model_4
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_work import \
    Danila_balka_text_recognize_work
from data.result.balka_prod import Balka_Prod


class Danila_balka_text_recognize_init_5:
    def __init__(self, yolov5_dir):
        danila_balka_text_recognize_model_4 = Danila_balka_text_recognize_model_4()
        model_4 = danila_balka_text_recognize_model_4.get_model(yolov5_dir)
        model_altai_4 = danila_balka_text_recognize_model_4.get_model_altai(yolov5_dir)
        danila_balka_text_recognize_model_3 = Danila_balka_text_recognize_model_3()
        model_3 = danila_balka_text_recognize_model_3.get_model(yolov5_dir)
        model_altai_3 = danila_balka_text_recognize_model_3.get_model_altai(yolov5_dir)
        self.prod_models = {}
        for balka_prod in Balka_Prod:
            if balka_prod == Balka_Prod.altai:
                self.prod_models[balka_prod] = Danila_balka_text_recognize_altai_work(
                    text_recognize_model=model_altai_3
                )
            else:
                self.prod_models[balka_prod] = Danila_balka_text_recognize_work(
                    text_recognize_model=model_4,
                    prod_coefficients=danila_balka_text_recognize_model_4.get_prod_coefficients(balka_prod)
                )

    def balka_text_recognize(self, balka_prod, img_cut, image_text_areas):
        return self.prod_models[balka_prod].balka_text_recognize(balka_prod, img_cut, image_text_areas)

