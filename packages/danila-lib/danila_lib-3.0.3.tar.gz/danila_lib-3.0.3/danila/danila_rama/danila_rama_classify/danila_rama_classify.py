from danila.danila_rama.danila_rama_classify.danila_rama_classify_prod import Danila_rama_classify_prod
from danila.danila_rama.danila_rama_classify.danila_rama_classify_prod_dop_detect import \
    Danila_rama_classify_prod_dop_detect


class Danila_rama_classify:
    def __init__(self, local, yolov5_dir, danila_rama_classify_params):
        self.danila_rama_classify_params = danila_rama_classify_params
        if self.danila_rama_classify_params.rama_classify_version == 1:
            self.danila_rama_classify = Danila_rama_classify_prod(local, yolov5_dir, self.danila_rama_classify_params.rama_classify_model)
        elif self.danila_rama_classify_params.rama_classify_version == 2:
            self.danila_rama_classify = Danila_rama_classify_prod_dop_detect(local, yolov5_dir, self.danila_rama_classify_params.rama_classify_model - 5)

    def rama_classify(self, img):
        return self.danila_rama_classify.rama_classify(img)

