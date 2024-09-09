import hashlib
import os
from datetime import datetime

import cv2

from data.neuro.Vagon_number_detect_class import Vagon_number_detect_class
from data.neuro.Vagon_number_recognize_yolo import Vagon_number_recognize_yolo
from data.neuro.local_models import *
from data.neuro.models import *


class Danila_vagon_text_recognize_base:
    def __init__(self, local, yolov5_dir, danila_vagon_text_recognize_params):


        print('reading and loading - VAGON_NUMBER_RECOGNIZE_MODEL')
        if local:
            if danila_vagon_text_recognize_params.vagon_text_recognize_version == 1:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, LOCAL_VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 2:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, LOCAL_VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 3:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, LOCAL_VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_3, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 4:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, LOCAL_VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_4, yolov5_dir)
        else:
            if danila_vagon_text_recognize_params.vagon_text_recognize_version == 1:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 2:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_2, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 3:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_3, yolov5_dir)
            elif danila_vagon_text_recognize_params.vagon_text_recognize_version == 4:
                self.vagon_number_recognize_model = Vagon_number_recognize_yolo(local, VAGON_NUMBER_RECOGNIZE_MODEL_ADDRESS_4, yolov5_dir)
        self.danila_vagon_text_recognize_params = danila_vagon_text_recognize_params


    def vagon_number_recognize(self, img, vagon_number_rects):
        return self.vagon_number_recognize_model.work_image(img, vagon_number_rects,
            self.danila_vagon_text_recognize_params.vagon_text_recognize_size_h,
            self.danila_vagon_text_recognize_params.vagon_text_recognize_size_w
                                                            )
