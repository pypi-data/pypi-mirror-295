import json
import os
import zipfile

import cv2
import requests
from urllib.parse import urlencode
import torch
import hashlib
from datetime import datetime
from data.neuro.letters_in_image import Letters_In_Image
from data.neuro.objs_in_image import Objs_In_Image
from data.result.Class_text import Class_text
from data.result.Label_area import Label_area
from data.result.Rama_prod import Rama_Prod, Rama_Prod_Conf


class Rama_prod_classify_dop_detect:

    def __init__(self, local, model_path, yolo_path, rama_detect_model):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        if local:
            self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
            self.rama_detect_model = torch.hub.load(yolo_path, 'custom', rama_detect_model, source='local')
        else:
            self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
            self.rama_detect_model = torch.hub.load(yolo_path, 'custom', rama_detect_model, source='local')

        # for every text_class try to recognize text from all areas of text_class, number_params is depends on class and prod, returns string


    def work_image(self, img, size, dop_size):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_name = 'img' + hash_str + '.jpg'
        cv2.imwrite(img_name, img)
        results = self.model([img_name], size = size)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        if len(res2) == 0:
            dop_rama_results = self.rama_detect_model([img_name], size=512)
            dop_rama_json_res = dop_rama_results.pandas().xyxy[0].to_json(orient="records")
            dop_rama_res2 = json.loads(dop_rama_json_res)
            if len(dop_rama_res2) == 0:
                result = Rama_Prod_Conf(Rama_Prod(7), 0.0)
            else:
                rama_img = img[int(dop_rama_res2[0]['ymin']):int(dop_rama_res2[0]['ymax']),
                           int(dop_rama_res2[0]['xmin']):int(dop_rama_res2[0]['xmax'])]
                cv2.imwrite('rama_' + img_name, rama_img)
                prod_results = self.model(['rama_' + img_name], size=dop_size)
                prod_json_res = prod_results.pandas().xyxy[0].to_json(orient="records")
                prod_res2 = json.loads(prod_json_res)
                os.remove('rama_' + img_name)
                if len(prod_res2) == 0:
                    result = Rama_Prod_Conf(Rama_Prod(7), 0.0)
                else:
                    res_index = prod_res2[0]['class']
                    res_conf = prod_res2[0]['confidence']
                    result = Rama_Prod_Conf(Rama_Prod(res_index), res_conf)
        else:
            res_index = res2[0]['class']
            res_conf = res2[0]['confidence']
            result = Rama_Prod_Conf(Rama_Prod(res_index), res_conf)
        os.remove(img_name)
        return result

    def classify(self, img, size_p, dop_size):
        self.model.max_det = 1
        rama_prod_conf = self.work_image(img, size_p, dop_size)
        return rama_prod_conf