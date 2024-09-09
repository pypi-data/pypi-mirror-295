from danila.danila_balka.danila_balka_text_detect.danila_balka_text_detect_base import Danila_balka_text_detect_base


class Danila_balka_text_detect:
    def __init__(self, local, yolov5_dir, danila_balka_text_detect_params):
        self.danila_balka_text_detect_params = danila_balka_text_detect_params
        self.danila_balka_text_detect = Danila_balka_text_detect_base(local, yolov5_dir,
                                                                    self.danila_balka_text_detect_params.balka_detect_version,
                                                                    self.danila_balka_text_detect_params.balka_text_detect_version)

    def balka_text_detect(self, img, rama_prod):
        return self.danila_balka_text_detect.balka_text_detect(img, rama_prod)

    def balka_rext_detect_cuts(self, img, rama_prod):
        return self.danila_balka_text_detect.balka_text_detect_cuts(img, rama_prod)