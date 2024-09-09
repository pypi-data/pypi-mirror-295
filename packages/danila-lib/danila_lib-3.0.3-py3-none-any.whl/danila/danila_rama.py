from danila.danila_rama.danila_rama_base import Danila_rama_base
from danila.danila_rama.danila_rama_redone import Danila_rama_redone


class Danila_rama:
    def __init__(self, local, yolov5_dir, danila_rama_params):
        if (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version < 3
        ) or (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version == 5
        ) or (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version == 7
        ) or (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version == 9
        ) or (danila_rama_params.danila_rama_text_recognize_params.rama_text_recognize_version == 11):
            self.danila_rama = Danila_rama_base(local, yolov5_dir, danila_rama_params)
        else:
            self.danila_rama = Danila_rama_redone(local, yolov5_dir, danila_rama_params)

    def rama_classify(self,img, detail):
        return self.danila_rama.rama_classify(img, detail)

    def rama_text_detect(self, img):
        return self.danila_rama.rama_text_detect(img)

    def rama_text_recognize(self, img, detail):
        return self.danila_rama.rama_text_recognize(img, detail)