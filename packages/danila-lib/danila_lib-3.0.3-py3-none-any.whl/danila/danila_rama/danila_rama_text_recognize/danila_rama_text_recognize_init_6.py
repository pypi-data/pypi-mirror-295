from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_1 import \
    Danila_rama_text_recognize_model_1
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_2 import \
    Danila_rama_text_recognize_model_2
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_3 import \
    Danila_rama_text_recognize_model_3
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_4 import \
    Danila_rama_text_recognize_model_4
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_work import Danila_rama_text_recognize_work
from data.result import Rama_prod



class Danila_rama_text_recognize_init_6:
    def __init__(self, yolov5_dir):
        danila_rama_text_recognize_model_1 = Danila_rama_text_recognize_model_1()
        model_1 = danila_rama_text_recognize_model_1.get_model(yolov5_dir)
        danila_rama_text_recognize_model_2 = Danila_rama_text_recognize_model_2()
        model_2 = danila_rama_text_recognize_model_2.get_model(yolov5_dir)
        danila_rama_text_recognize_model_3 = Danila_rama_text_recognize_model_3()
        model_3 = danila_rama_text_recognize_model_3.get_model(yolov5_dir)
        danila_rama_text_recognize_model_4 = Danila_rama_text_recognize_model_4()
        model_4 = danila_rama_text_recognize_model_4.get_model(yolov5_dir)
        self.prod_models = {}
        for rama_prod in Rama_prod.Rama_Prod:
            if rama_prod == Rama_prod.Rama_Prod.altai:
                self.prod_models[rama_prod] = Danila_rama_text_recognize_work(
                    text_recognize_model=model_3,
                    prod_coefficients=danila_rama_text_recognize_model_3.get_prod_coefficients(rama_prod)
                )
            elif rama_prod == Rama_prod.Rama_Prod.tihvin:
                self.prod_models[rama_prod] = Danila_rama_text_recognize_work(
                    text_recognize_model=model_3,
                    prod_coefficients=danila_rama_text_recognize_model_3.get_prod_coefficients(rama_prod)
                )
            elif rama_prod == Rama_prod.Rama_Prod.ruzhimmash:
                self.prod_models[rama_prod] = Danila_rama_text_recognize_work(
                    text_recognize_model=model_2,
                    prod_coefficients=danila_rama_text_recognize_model_2.get_prod_coefficients(rama_prod)
                )
            else:
                self.prod_models[rama_prod] = Danila_rama_text_recognize_work(
                    text_recognize_model=model_4,
                    prod_coefficients=danila_rama_text_recognize_model_4.get_prod_coefficients(rama_prod)
                )

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        return self.prod_models[rama_prod].rama_text_recognize(img_cut, image_text_areas)

    def get_number_length(self, rama_prod):
        return self.prod_models[rama_prod].prod_coefficients.number_coefficients.length
