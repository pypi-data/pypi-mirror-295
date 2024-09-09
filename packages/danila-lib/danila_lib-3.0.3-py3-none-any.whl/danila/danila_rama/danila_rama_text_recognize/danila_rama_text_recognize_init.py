from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_1 import \
    Danila_rama_text_recognize_init_1
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_2 import \
    Danila_rama_text_recognize_init_2
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_3 import \
    Danila_rama_text_recognize_init_3
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_4 import \
    Danila_rama_text_recognize_init_4
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_5 import \
    Danila_rama_text_recognize_init_5
from danila.danila_rama.danila_rama_text_recognize.danila_rama_text_recognize_init_6 import \
    Danila_rama_text_recognize_init_6


class Danila_rama_text_recognize_init:
    def __init__(self, yolov5_dir, rama_text_recognize_version):
        if rama_text_recognize_version == 1:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_1(yolov5_dir=yolov5_dir)
        elif rama_text_recognize_version == 2:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_2(yolov5_dir=yolov5_dir)
        elif rama_text_recognize_version == 3:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_3(yolov5_dir=yolov5_dir)
        elif rama_text_recognize_version == 4:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_4(yolov5_dir=yolov5_dir)
        elif rama_text_recognize_version == 5:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_5(yolov5_dir=yolov5_dir)
        elif rama_text_recognize_version == 6:
            self.danila_rama_text_recognize_init = Danila_rama_text_recognize_init_6(yolov5_dir=yolov5_dir)

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        return self.danila_rama_text_recognize_init.rama_text_recognize(rama_prod, img_cut, image_text_areas)

    def get_number_length(self, rama_prod):
        return self.danila_rama_text_recognize_init.get_number_length(rama_prod)


