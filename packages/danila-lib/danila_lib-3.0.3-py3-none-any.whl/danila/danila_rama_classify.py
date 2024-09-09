from danila.danila_rama.danila_rama_classify.danila_rama_classify_prod import Danila_rama_classify_prod


class Danila_rama_classify:
    def __init__(self, local, yolov5_dir, danila_rama_classify_params):
        self.danila_rama_classify_params = danila_rama_classify_params
        if self.danila_rama_classify_params.rama_classify_version == 1:
            self.danila_rama_classify = Danila_rama_classify_prod(local, yolov5_dir, self.danila_rama_classify_params.rama_classify_model)

    def rama_classify(self, img):
        return self.danila_rama_classify.rama_classify(img)

