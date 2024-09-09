from danila.danila_detail.Danila_detail_CNN import Danila_detail_CNN
from danila.danila_detail.Danila_detail_yolo_dop_yolo_dop_CNN import Danila_detail_yolo_dop_yolo_dop_CNN


class Danila_detail():
    def __init__(self, local, danila_detail_params, yolo_dir = ''):
        self.danila_detail_params = danila_detail_params
        if (danila_detail_params.model_version == 1):
            self.danila_detail = Danila_detail_CNN(local, danila_detail_params.CNN_model_version)
        elif (danila_detail_params.model_version == 2):
            self.danila_detail = Danila_detail_yolo_dop_yolo_dop_CNN(local, yolo_dir, danila_detail_params.CNN_model_version)



    def detail_classify(self, img):
        return self.danila_detail.detail_classify(img)

