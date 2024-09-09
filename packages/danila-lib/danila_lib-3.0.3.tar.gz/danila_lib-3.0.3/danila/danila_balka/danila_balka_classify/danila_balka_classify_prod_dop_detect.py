from data.neuro.Balka_prod_classify_class import Balka_prod_classify_class
from data.neuro.Balka_prod_classify_class_dop_detect import Balka_prod_classify_class_dop_detect
from data.neuro.local_models import *
from data.neuro.models import *


class Danila_balka_classify_prod_dop_detect:
    def __init__(self, yolov5_dir, balka_classify_model):
        yolo_path = yolov5_dir
        if balka_classify_model == 1:
            balka_prod_classify_model_path = LOCAL_BALKA_CLASSIFY_MODEL_ADDRESS
            self.size = 640
        elif balka_classify_model == 2:
            balka_prod_classify_model_path = LOCAL_BALKA_CLASSIFY_MODEL_ADDRESS_2
            self.size = 416
            self.size_detect = 352

        print('reading and loading - BALKA_PROD_CLASSIFY_MODEL')
        self.balka_prod_classify_model = Balka_prod_classify_class_dop_detect(balka_prod_classify_model_path, LOCAL_BALKA_DETECT_MODEL_ADDRESS, yolo_path)

    def balka_classify(self, img):
        balka_prod_conf = self.balka_prod_classify_model.classify(img, self.size, self.size_detect)
        return balka_prod_conf