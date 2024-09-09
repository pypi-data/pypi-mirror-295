from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init import \
    Danila_balka_text_recognize_init
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_prod_redone import \
    Danila_balka_text_recognize_prod_redone
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_year_post import \
    Danila_balka_text_recognize_year_post


class Danila_balka_text_recognize:
    def __init__(self, yolov5_dir, danila_balka_text_recognize_params):
        danila_balka_text_recognize = Danila_balka_text_recognize_init(
            yolov5_dir=yolov5_dir,
            balka_text_recognize_version=danila_balka_text_recognize_params.balka_text_recognize_model_version
        )
        if danila_balka_text_recognize_params.prod_redone:
            danila_balka_text_recognize = Danila_balka_text_recognize_prod_redone(danila_balka_text_recognize)
        if danila_balka_text_recognize_params.year_post:
            danila_balka_text_recognize = Danila_balka_text_recognize_year_post(danila_balka_text_recognize)
        self.danila_balka_text_recognize = danila_balka_text_recognize

    def balka_text_recognize(self, balka_prod, img_cuts, img_text_areas_2_balkas):
        return self.danila_balka_text_recognize.balka_text_recognize(balka_prod,img_cuts,img_text_areas_2_balkas)