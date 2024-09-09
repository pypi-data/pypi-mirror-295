from danila.danila_balka.danila_balka_classify.danila_balka_classify_prod import Danila_balka_classify_prod


class Danila_balka_classify:
    def __init__(self, local, yolov5_dir, danila_balka_classify_params):
        self.danila_balka_classify_params = danila_balka_classify_params
        if self.danila_balka_classify_params.balka_classify_version == 1:
            self.danila_balka_classify = Danila_balka_classify_prod(local, yolov5_dir, self.danila_balka_classify_params.balka_classify_model)


    def balka_classify(self, img):
        return self.danila_balka_classify.balka_classify(img)