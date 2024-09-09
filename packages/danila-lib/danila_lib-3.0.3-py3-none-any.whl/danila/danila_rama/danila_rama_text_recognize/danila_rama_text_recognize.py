from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init import \
    Danila_rama_text_recognize_init
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_number_shift import \
    Danila_rama_text_recognize_number_shift
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_prod_redone import \
    Danila_rama_text_recognize_prod_redone
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_year_post import \
    Danila_rama_text_recognize_year_post


class Danila_rama_text_recognize:
    def __init__(self, yolov5_dir, danila_rama_text_recognize_params):
        danila_rama_text_recognize = Danila_rama_text_recognize_init(
            yolov5_dir=yolov5_dir,
            rama_text_recognize_version=danila_rama_text_recognize_params.rama_text_recognize_model_version
        )
        if danila_rama_text_recognize_params.prod_redone:
            danila_rama_text_recognize = Danila_rama_text_recognize_prod_redone(danila_rama_text_recognize)
        if danila_rama_text_recognize_params.number_shift:
            danila_rama_text_recognize = Danila_rama_text_recognize_number_shift(danila_rama_text_recognize)
        if danila_rama_text_recognize_params.year_post:
            danila_rama_text_recognize = Danila_rama_text_recognize_year_post(danila_rama_text_recognize)
        self.danila_rama_text_recognize = danila_rama_text_recognize


    def rama_text_recognize(self, rama_prod, img_cut, img_text_areas):
        return self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, img_text_areas)