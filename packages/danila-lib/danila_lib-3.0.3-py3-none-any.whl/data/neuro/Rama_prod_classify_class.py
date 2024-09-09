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


class Rama_prod_classify_class:

    def __init__(self, local, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        if local:
            self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
        else:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = model_path  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'prod_classify.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            # weights_file_path = model_name + '_weights.pt'
            self.model = torch.hub.load(yolo_path, 'custom', 'prod_classify.pt', source='local')

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
            result = Rama_Prod_Conf(Rama_Prod(7), 0.0)
        else:
            res_index = res2[0]['class']
            res_conf = res2[0]['confidence']
            result = Rama_Prod_Conf(Rama_Prod(res_index), res_conf)
        os.remove(img_name)
        return result

    def classify(self, img, size_p):
        self.model.max_det = 1
        rama_prod_conf = self.work_image(img, size_p)
        if rama_prod_conf.rama_prod == Rama_Prod.no_rama:
            sizes = [224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 576, 608, 640, 672, 704, 736, 768, 800]
            flag = True
            for size in sizes:
                if flag:
                    rama_prod_conf1 = self.work_image(img, size)
                    flag = (rama_prod_conf1.rama_prod == Rama_Prod.no_rama)
                    if not(flag):
                        rama_prod_conf = rama_prod_conf1
        return rama_prod_conf