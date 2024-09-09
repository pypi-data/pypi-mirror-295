from data.neuro.Balka_prod_classify_class import Balka_prod_classify_class
from data.neuro.local_models import *
from data.neuro.models import *


class Danila_balka_classify_prod:
    def __init__(self, local, yolov5_dir, balka_classify_model):
        yolo_path = yolov5_dir
        if local:
            if balka_classify_model == 1:
                balka_prod_classify_model_path = LOCAL_BALKA_CLASSIFY_MODEL_ADDRESS
                self.size = 640
            if balka_classify_model == 2:
                balka_prod_classify_model_path = LOCAL_BALKA_CLASSIFY_MODEL_ADDRESS_2
                self.size = 736
        else:
            if balka_classify_model == 1:
                balka_prod_classify_model_path = BALKA_CLASSIFY_MODEL_ADDRESS
                self.size = 640

        print('reading and loading - BALKA_PROD_CLASSIFY_MODEL')
        self.balka_prod_classify_model = Balka_prod_classify_class(local, balka_prod_classify_model_path, yolo_path)

    def balka_classify(self, img):
        balka_prod_conf = self.balka_prod_classify_model.classify(img, self.size)
        return balka_prod_conf