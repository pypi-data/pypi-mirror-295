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


class Balka_prod_classify_class_dop_detect:

    def __init__(self, model_path, model_detect_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
        self.model_detect = torch.hub.load(yolo_path, 'custom', model_detect_path, source='local')
        # for every text_class try to recognize text from all areas of text_class, number_params is depends on class and prod, returns string


    def work_image(self, img, size, size_detect):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_name = 'img' + hash_str + '.jpg'
        cv2.imwrite(img_name, img)
        results = self.model([img_name], size = size)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        if len(res2) == 0:
            results_balka = self.model_detect([img_name])
            json_res_balka = results_balka.pandas().xyxy[0].to_json(orient="records")
            res2_balka = json.loads(json_res_balka)
            if len(res2_balka) == 0:
                result = Balka_Prod_Conf(Balka_Prod(5), 0.0)
            else:
                prods = []
                i = 1
                for balka in res2_balka:
                    balka_img = img[int(balka['ymin']):int(balka['ymax']), int(balka['xmin']):int(balka['xmax'])]
                    cv2.imwrite(str(i) + 'balka.jpg', balka_img)
                    results_3 = self.model([str(i) + 'balka.jpg'], size=size_detect)
                    json_res_3 = results_3.pandas().xyxy[0].to_json(orient="records")
                    res3 = json.loads(json_res_3)
                    if len(res3) > 0:
                        prods.append(res3[0])
                    os.remove(str(i) + 'balka.jpg')
                    i += 1
                prods.sort(key=lambda prod: prod['confidence'], reverse=True)
                if len(prods) == 0:
                    result = Balka_Prod_Conf(Balka_Prod(5), 0.0)
                else:
                    res2 = prods
                    res_index = res2[0]['class']
                    res_conf = res2[0]['confidence']
                    result = Balka_Prod_Conf(Balka_Prod(res_index), res_conf)
        else:
            res_index = res2[0]['class']
            res_conf = res2[0]['confidence']
            result = Balka_Prod_Conf(Balka_Prod(res_index), res_conf)
        os.remove(img_name)
        return result

    def classify(self, img, size, size_detect):
        self.model.max_det = 1
        balka_prod_conf = self.work_image(img, size, size_detect)
        return balka_prod_conf