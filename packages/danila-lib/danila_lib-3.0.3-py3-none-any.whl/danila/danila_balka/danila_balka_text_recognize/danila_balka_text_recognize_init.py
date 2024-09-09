from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init_1 import \
    Danila_balka_text_recognize_init_1
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init_2 import \
    Danila_balka_text_recognize_init_2
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init_3 import \
    Danila_balka_text_recognize_init_3
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init_4 import \
    Danila_balka_text_recognize_init_4
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_init_5 import \
    Danila_balka_text_recognize_init_5


class Danila_balka_text_recognize_init:
    def __init__(self, yolov5_dir, balka_text_recognize_version):
        if balka_text_recognize_version == 1:
            self.danila_balka_text_recognize_init = Danila_balka_text_recognize_init_1(yolov5_dir=yolov5_dir)
        elif balka_text_recognize_version == 2:
            self.danila_balka_text_recognize_init = Danila_balka_text_recognize_init_2(yolov5_dir=yolov5_dir)
        elif balka_text_recognize_version == 3:
            self.danila_balka_text_recognize_init = Danila_balka_text_recognize_init_3(yolov5_dir=yolov5_dir)
        elif balka_text_recognize_version == 4:
            self.danila_balka_text_recognize_init = Danila_balka_text_recognize_init_4(yolov5_dir=yolov5_dir)
        elif balka_text_recognize_version == 5:
            self.danila_balka_text_recognize_init = Danila_balka_text_recognize_init_5(yolov5_dir=yolov5_dir)

    def balka_text_recognize(self, balka_prod, img_cut, image_text_areas):
        return self.danila_balka_text_recognize_init.balka_text_recognize(balka_prod, img_cut, image_text_areas)


