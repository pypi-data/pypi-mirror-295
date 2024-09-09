from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_base import Danila_balka_text_recognize_base
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize_redone import Danila_balka_text_recognize_redone



class Danila_balka_text_recognize:
    def __init__(self, local, yolov5_dir, danila_balka_text_recognize_params):
        self.danila_balka_text_recognize_params = danila_balka_text_recognize_params
        if (self.danila_balka_text_recognize_params.balka_text_recognize_version < 3) | (self.danila_balka_text_recognize_params.balka_text_recognize_version == 5):
            self.danila_balka_text_recognize = Danila_balka_text_recognize_base(local, yolov5_dir,
                                                                    self.danila_balka_text_recognize_params.balka_text_recognize_version
                                                                    )
        else:
            self.danila_balka_text_recognize = Danila_balka_text_recognize_redone(local, yolov5_dir,
                                                                                self.danila_balka_text_recognize_params.balka_text_recognize_version
                                                                                )

    def balka_text_recognize(self, balka_prod, img_cuts, img_text_areas_2_balkas):
        return self.danila_balka_text_recognize.balka_text_recognize(_balka_prod=balka_prod, img_cuts=img_cuts,
                                                                     image_text_areas_2_balkas=img_text_areas_2_balkas)