
from data.neuro.Detail_classify_class import Detail_classify_class
from data.neuro.local_models import *
from data.neuro.models import DETAIL_CLASSIFY_MODEL_ADDRESS, DETAIL_CLASSIFY_MODEL_ADDRESS_2
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_detail_CNN():
    def __init__(self, local, CNN_model_version):
        if local:
            if CNN_model_version == 1:
                detail_classify_model_path = LOCAL_DETAIL_CLASSIFY_MODEL_ADDRESS
            else:
                detail_classify_model_path = LOCAL_DETAIL_CLASSIFY_MODEL_ADDRESS_2
            print('reading and loading - DETAIL_CLASSIFY_MODEL')
            self.detail_classify_model = Detail_classify_class(local, detail_classify_model_path)
        else:
            if CNN_model_version == 1:
                detail_classify_model_path = DETAIL_CLASSIFY_MODEL_ADDRESS
            else:
                detail_classify_model_path = DETAIL_CLASSIFY_MODEL_ADDRESS_2
            print('reading and loading - DETAIL_CLASSIFY_MODEL')
            self.detail_classify_model = Detail_classify_class(local, detail_classify_model_path)


    def detail_classify(self, img):
        class_detail_conf = self.detail_classify_model.classify(img)
        detail = Text_recognize_result(
            Text_cut_recognize_result(class_detail_conf.class_detail.name, class_detail_conf.conf))
        return detail
