import json
import os

import cv2
import torch
import zipfile
import requests
from urllib.parse import urlencode
from data.result import Rect, Yolo_label_rect

"""module for detecting rama"""
class Rama_detect_class:
    """module for detecting rama"""

    # reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, local, model_path, yolo_path, sort_by_square = False):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.sort_by_square = sort_by_square
        if local:
            self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

            # self.model.max_det = 1
        else:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = model_path  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'rama_detect.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'rama_detect.pt'
            self.model = torch.hub.load(yolo_path, 'custom', weights_file_path, source='local')
            # self.model.max_det = 1



    #получить JSON с результатами yolo
    def work_img(self, img_path):
        """get JSON with yolo_results from img from img_path"""
        results = self.model([img_path])
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        return res2

    # получить координаты прямоугольника с рамой
    def rama_detect(self, img_path):
        """get Rect object with rama coordinates from img from img_path"""
        json_res_pred = self.work_img(img_path)
        if self.sort_by_square:
            json_res = sorted(json_res_pred, key = lambda rama: (float(rama['xmax']) - float(rama['xmin']))*(float(rama['ymax']) - float(rama['ymin'])), reverse=True)
        else:
            json_res = json_res_pred
        rect = Rect.Rect.get_rect_from_yolo_json(json_res)
        return rect


