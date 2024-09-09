from danila.danila_rama.danila_rama_text_detect.danila_rama_text_detect_base import Danila_rama_text_detect_base


class Danila_rama_text_detect:
    def __init__(self, local, yolov5_dir, danila_rama_text_detect_params):
        self.danila_rama_text_detect_params = danila_rama_text_detect_params
        self.danila_rama_text_detect = Danila_rama_text_detect_base(local, yolov5_dir,
                                                                    self.danila_rama_text_detect_params.rama_detect_version,
                                                                    self.danila_rama_text_detect_params.rama_text_detect_version)

    def rama_text_detect(self, img, rama_prod):
        return self.danila_rama_text_detect.rama_text_detect(img, rama_prod)

    def rama_rext_detect_cuts(self, img, rama_prod):
        return self.danila_rama_text_detect.rama_text_detect_cuts(img, rama_prod)