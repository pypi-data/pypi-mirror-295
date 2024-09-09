import hashlib
import os
from datetime import datetime

import cv2

from data.neuro.Vagon_number_detect_class import Vagon_number_detect_class
from data.neuro.local_models import *
from data.neuro.models import VAGON_NUMBER_DETECT_MODEL_ADDRESS, VAGON_NUMBER_DETECT_MODEL_ADDRESS_2


class Danila_vagon_text_detect_base:
    def __init__(self, local, yolov5_dir, vagon_text_detect_params):
        print('reading and loading - VAGON_NUMBER_DETECT_MODEL')
        if local:
            if vagon_text_detect_params.vagon_text_detect_version == 1:
                self.vagon_number_detect_model = Vagon_number_detect_class(local, LOCAL_VAGON_NUMBER_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif vagon_text_detect_params.vagon_text_detect_version == 2:
                self.vagon_number_detect_model = Vagon_number_detect_class(local, LOCAL_VAGON_NUMBER_DETECT_MODEL_ADDRESS_2, yolov5_dir)
        else:
            if vagon_text_detect_params.vagon_text_detect_version == 1:
                self.vagon_number_detect_model = Vagon_number_detect_class(local, VAGON_NUMBER_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif vagon_text_detect_params.vagon_text_detect_version == 2:
                self.vagon_number_detect_model = Vagon_number_detect_class(local, VAGON_NUMBER_DETECT_MODEL_ADDRESS_2, yolov5_dir)


    def vagon_number_detect(self, img):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        number_rects = self.vagon_number_detect_model.vagon_rama_detect(initial_image_path, 512)
        if len(number_rects) == 0:
            os.remove(initial_image_path)
            return img
        img_with_number = img.copy()
        for number_rect in number_rects:
            cv2.rectangle(img_with_number, (number_rect.xmin, number_rect.ymin), (number_rect.xmax, number_rect.ymax), (0, 0, 255), 2)
            cv2.putText(img_with_number, 'number', (number_rect.xmin, number_rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        os.remove(initial_image_path)
        return img_with_number

    def vagon_number_detect_rects(self, img):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        number_rects = self.vagon_number_detect_model.vagon_rama_detect(initial_image_path, 512)
        os.remove(initial_image_path)
        return number_rects