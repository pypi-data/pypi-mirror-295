from data.neuro import rama_a_b_p_r_t_text_recognize_model_balka_params
from data.neuro.balka_text_recognize_yolo import Balka_Text_Recognize_yolo, Balka_text_recognize_params, \
    Balka_text_cut_recognize_params
from data.neuro.local_models import *
from data.neuro.models import RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2
from data.neuro.text_recognize_yolo import Text_Recognize_yolo
from data.result import Rama_prod
from data.result.Class_text import Class_text
from data.result.Rect import Rect
from data.result.balka_prod import Balka_Prod


class Danila_balka_text_recognize_base:
    def __init__(self, yolov5_dir, balka_text_recognize_version):
        if balka_text_recognize_version == 1:
            self.prod_coefficients = {
                    Balka_Prod.altai: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                 Balka_text_cut_recognize_params(4, 64, 128),
                                                                 Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.begickaya: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                     Balka_text_cut_recognize_params(2, 64, 64),
                                                                     Balka_text_cut_recognize_params(2, 64, 96)),
                    Balka_Prod.promlit: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                   Balka_text_cut_recognize_params(2, 64, 64),
                                                                   Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.ruzhimmash: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 192),
                                                                      Balka_text_cut_recognize_params(4, 64, 96),
                                                                      Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.tihvin: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                  Balka_text_cut_recognize_params(4, 64, 128),
                                                                  Balka_text_cut_recognize_params(2, 64, 64))
                }
            print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
            self.text_recognize_model = Balka_Text_Recognize_yolo(LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS, yolov5_dir, self.prod_coefficients)
        elif balka_text_recognize_version == 2:
            self.prod_coefficients = {
                    Balka_Prod.altai: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                 Balka_text_cut_recognize_params(4, 64, 128),
                                                                 Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.begickaya: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                     Balka_text_cut_recognize_params(2, 64, 64),
                                                                     Balka_text_cut_recognize_params(2, 64, 96)),
                    Balka_Prod.promlit: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                   Balka_text_cut_recognize_params(2, 64, 64),
                                                                   Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.ruzhimmash: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 192),
                                                                      Balka_text_cut_recognize_params(4, 64, 96),
                                                                      Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.tihvin: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 64, 160),
                                                                  Balka_text_cut_recognize_params(4, 64, 128),
                                                                  Balka_text_cut_recognize_params(2, 64, 64))
                }
            print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
            self.text_recognize_model = Balka_Text_Recognize_yolo(LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir, self.prod_coefficients)
        elif balka_text_recognize_version == 5:
            self.prod_coefficients = {
                    Balka_Prod.altai: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 128, 128),
                                                                 Balka_text_cut_recognize_params(4, 128, 128),
                                                                 Balka_text_cut_recognize_params(2, 32, 32)),
                    Balka_Prod.begickaya: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 160, 160),
                                                                     Balka_text_cut_recognize_params(2, 64, 64),
                                                                     Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.promlit: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 96, 96),
                                                                   Balka_text_cut_recognize_params(2, 128, 128),
                                                                   Balka_text_cut_recognize_params(2, 32, 32)),
                    Balka_Prod.ruzhimmash: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 128, 128),
                                                                      Balka_text_cut_recognize_params(4, 96, 96),
                                                                      Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.tihvin: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 96, 96),
                                                                  Balka_text_cut_recognize_params(4, 96, 96),
                                                                  Balka_text_cut_recognize_params(2, 64, 64))
                }
            print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
            self.text_recognize_model = Balka_Text_Recognize_yolo(LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir, self.prod_coefficients)
        elif balka_text_recognize_version == 7:
            self.prod_coefficients = {
                    Balka_Prod.altai: Balka_text_recognize_params(
                        Balka_text_cut_recognize_params(
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_NUMBER_LENGTH,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_NUMBER_HEIGHT,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_NUMBER_WIDTH
                        ),
                        Balka_text_cut_recognize_params(
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_PROD_LENGTH,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_PROD_HEIGHT,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_PROD_WIDTH
                        ),
                        Balka_text_cut_recognize_params(
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_YEAR_LENGTH,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_YEAR_HEIGHT,
                            rama_a_b_p_r_t_text_recognize_model_balka_params.ALTAI_YEAR_WIDTH
                        )
                    ),
                    Balka_Prod.begickaya: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 160, 160),
                                                                     Balka_text_cut_recognize_params(2, 64, 64),
                                                                     Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.promlit: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 96, 96),
                                                                   Balka_text_cut_recognize_params(2, 128, 128),
                                                                   Balka_text_cut_recognize_params(2, 32, 32)),
                    Balka_Prod.ruzhimmash: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 128, 128),
                                                                      Balka_text_cut_recognize_params(4, 96, 96),
                                                                      Balka_text_cut_recognize_params(2, 64, 64)),
                    Balka_Prod.tihvin: Balka_text_recognize_params(Balka_text_cut_recognize_params(5, 96, 96),
                                                                  Balka_text_cut_recognize_params(4, 96, 96),
                                                                  Balka_text_cut_recognize_params(2, 64, 64))
                }
            print('reading and loading - BALKA_TEXT_RECOGNIZE_MODEL')
            self.text_recognize_model = Balka_Text_Recognize_yolo(LOCAL_RAMA_TEXT_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir, self.prod_coefficients)



    def balka_text_recognize(self, _balka_prod, img_cuts, image_text_areas_2_balkas):
        label_area = self.text_recognize_model.work_image_cut(
            _balka_prod=_balka_prod, image_text_areas_2_half_balkas=image_text_areas_2_balkas, image_balka_cuts=img_cuts
        )
        res_labels = {}
        (number_text, number_conf) = label_area.labels[Class_text.number]
        res_labels['number'] = (number_text, number_conf)
        (year_text, year_conf) = label_area.labels[Class_text.year]
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('24', 0.25)
        return res_labels


