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
from data.result.balka_prod import Balka_Prod_Conf, Balka_Prod


class Balka_prod_classify_class:

    def __init__(self, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

        # for every text_class try to recognize text from all areas of text_class, number_params is depends on class and prod, returns string


    def work_image(self, img, size):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_name = 'img' + hash_str + '.jpg'
        cv2.imwrite(img_name, img)
        results = self.model([img_name], size = size)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        if len(res2) == 0:
            result = Balka_Prod_Conf(Balka_Prod(5), 0.0)
        else:
            res_index = res2[0]['class']
            res_conf = res2[0]['confidence']
            result = Balka_Prod_Conf(Balka_Prod(res_index), res_conf)
        os.remove(img_name)
        return result

    def classify(self, img, size):
        self.model.max_det = 1
        balka_prod_conf = self.work_image(img, size)
        if balka_prod_conf.balka_prod == Balka_Prod.no_balka:
            sizes = [224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768, 800]
            flag = True
            for size in sizes:
                if flag:
                    balka_prod_conf1 = self.work_image(img, size)
                    flag = (balka_prod_conf1.balka_prod == Balka_Prod.no_balka)
                    if not (flag):
                        balka_prod_conf = balka_prod_conf1
        return balka_prod_conf