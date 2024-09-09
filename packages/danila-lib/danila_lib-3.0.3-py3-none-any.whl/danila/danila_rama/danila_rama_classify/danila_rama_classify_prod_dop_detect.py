from data.neuro.Rama_prod_classify_class import Rama_prod_classify_class
from data.neuro.Rama_prod_classify_dop_detect import Rama_prod_classify_dop_detect
from data.neuro.local_models import *
from data.neuro.models import RAMA_PROD_CLASSIFY_MODEL_ADDRESS, RAMA_PROD_CLASSIFY_MODEL_ADDRESS_2, \
    RAMA_PROD_CLASSIFY_MODEL_ADDRESS_3


class Danila_rama_classify_prod_dop_detect:
    def __init__(self, local, yolov5_dir, rama_classify_model):
        yolo_path = yolov5_dir
        if local:
            if rama_classify_model == 3:
                rama_prod_classify_model_path = LOCAL_RAMA_PROD_CLASSIFY_MODEL_ADDRESS_3
                self.size = 480
                self.dop_size = 256
            elif rama_classify_model == 4:
                rama_prod_classify_model_path = LOCAL_RAMA_PROD_CLASSIFY_MODEL_ADDRESS_4
                self.size = 608
                self.dop_size = 224
            elif rama_classify_model == 5:
                rama_prod_classify_model_path = LOCAL_RAMA_PROD_CLASSIFY_MODEL_ADDRESS_5
                self.size = 608
                self.dop_size = 224
        else:
            if rama_classify_model == 5:
                rama_prod_classify_model_path = LOCAL_RAMA_PROD_CLASSIFY_MODEL_ADDRESS_5
                self.size = 608
        print('reading and loading - RAMA_PROD_CLASSIFY_MODEL')
        self.rama_prod_classify_model = Rama_prod_classify_dop_detect(local, rama_prod_classify_model_path, yolo_path, LOCAL_RAMA_DETECT_MODEL_ADDRESS)

    def rama_classify(self, img):
        rama_prod_conf = self.rama_prod_classify_model.classify(img, self.size, self.dop_size)
        return rama_prod_conf