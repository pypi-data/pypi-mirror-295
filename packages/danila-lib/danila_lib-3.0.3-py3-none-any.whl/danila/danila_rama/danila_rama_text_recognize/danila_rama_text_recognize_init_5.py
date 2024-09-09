from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_3 import \
    Danila_rama_text_recognize_model_3
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_model_4 import \
    Danila_rama_text_recognize_model_4
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_work import Danila_rama_text_recognize_work
from data.result import Rama_prod



class Danila_rama_text_recognize_init_5:
    def __init__(self, yolov5_dir):
        danila_rama_text_recognize_model = Danila_rama_text_recognize_model_4()
        model = danila_rama_text_recognize_model.get_model(yolov5_dir)
        self.prod_models = {}
        for rama_prod in Rama_prod.Rama_Prod:
            self.prod_models[rama_prod] = Danila_rama_text_recognize_work(
                text_recognize_model=model,
                prod_coefficients=danila_rama_text_recognize_model.get_prod_coefficients(rama_prod)
            )

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        return self.prod_models[rama_prod].rama_text_recognize(img_cut, image_text_areas)

    def get_number_length(self, rama_prod):
        return self.prod_models[rama_prod].prod_coefficients.number_coefficients.length
