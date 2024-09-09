from danila.danila_balka.danila_balka_base import Danila_balka_base
from danila.danila_balka.danila_balka_redone import Danila_balka_redone


class Danila_balka:
    def __init__(self, yolov5_dir, danila_balka_params):
        if danila_balka_params.danila_balka_text_recognize_params.prod_redone:
            self.danila_balka = Danila_balka_redone(yolov5_dir, danila_balka_params)
        else:
            self.danila_balka = Danila_balka_base(yolov5_dir, danila_balka_params)

    def balka_classify(self,img, detail):
        return self.danila_balka.balka_classify(img, detail)

    def balka_text_detect(self, img):
        return self.danila_balka.balka_text_detect(img)

    def balka_text_recognize(self, img, detail):
        return self.danila_balka.balka_text_recognize(img, detail)