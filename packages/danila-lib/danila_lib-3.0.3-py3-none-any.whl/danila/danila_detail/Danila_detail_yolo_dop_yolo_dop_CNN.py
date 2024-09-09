
from data.neuro.Detail_classify_class import Detail_classify_class
from data.neuro.Detail_classify_yolo_dop_yolo_dop_CNN import Detail_classify_yolo_dop_yolo_dop_CNN
from data.neuro.local_models import *
from data.neuro.models import DETAIL_CLASSIFY_MODEL_ADDRESS, DETAIL_CLASSIFY_MODEL_ADDRESS_2, \
    DETAIL_CLASSIFY_YOLO_MODEL_ADDRESS, DETAIL_CLASSIFY_BALKA_MODEL_ADDRESS, DETAIL_CLASSIFY_RAMA_MODEL_ADDRESS, \
    DETAIL_CLASSIFY_VAGON_MODEL_ADDRESS
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_detail_yolo_dop_yolo_dop_CNN():
    def __init__(self, local, yolo_dir, CNN_model_version):
        if local:
            if CNN_model_version == 1:
                detail_classify_model_path = LOCAL_DETAIL_CLASSIFY_MODEL_ADDRESS_2
            print('reading and loading - DETAIL_CLASSIFY_MODEL')
            self.detail_classify_model = Detail_classify_yolo_dop_yolo_dop_CNN(local, yolo_dir= yolo_dir,
                                                                               detail_classify_CNN=detail_classify_model_path,
                                                                               detail_classify_yolo= LOCAL_DETAIL_CLASSIFY_YOLO_MODEL_ADDRESS,
                                                                               balka_detect= LOCAL_DETAIL_CLASSIFY_BALKA_MODEL_ADDRESS,
                                                                               rama_detect= LOCAL_DETAIL_CLASSIFY_RAMA_MODEL_ADDRESS,
                                                                               vagon_detect= LOCAL_DETAIL_CLASSIFY_VAGON_MODEL_ADDRESS)
        else:
            if CNN_model_version == 1:
                detail_classify_model_path = DETAIL_CLASSIFY_MODEL_ADDRESS_2
            print('reading and loading - DETAIL_CLASSIFY_MODEL')
            self.detail_classify_model = Detail_classify_yolo_dop_yolo_dop_CNN(local, yolo_dir= yolo_dir,
                                                                               detail_classify_CNN=detail_classify_model_path,
                                                                               detail_classify_yolo= DETAIL_CLASSIFY_YOLO_MODEL_ADDRESS,
                                                                               balka_detect= DETAIL_CLASSIFY_BALKA_MODEL_ADDRESS,
                                                                               rama_detect= DETAIL_CLASSIFY_RAMA_MODEL_ADDRESS,
                                                                               vagon_detect= DETAIL_CLASSIFY_VAGON_MODEL_ADDRESS)




    def detail_classify(self, img):
        class_detail_conf = self.detail_classify_model.classify(img)
        detail = Text_recognize_result(
            Text_cut_recognize_result(class_detail_conf.class_detail.name, class_detail_conf.conf))
        return detail
