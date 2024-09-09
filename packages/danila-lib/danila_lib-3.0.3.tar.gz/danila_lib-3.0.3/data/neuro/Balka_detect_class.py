import json
import os

import cv2
import torch
import zipfile
import requests
from urllib.parse import urlencode
from data.result import Rect, Yolo_label_rect

"""module for detecting rama"""
class Balka_detect_class:
    """module for detecting rama"""

    # reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

    #получить JSON с результатами yolo
    def work_img(self, img_path):
        """get JSON with yolo_results from img from img_path"""
        results = self.model([img_path])
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        return res2

    # получить координаты прямоугольника с рамой
    def balka_detect(self, img_path):
        """get Rect object with rama coordinates from img from img_path"""
        self.model.max_det = 2
        json_res = self.work_img(img_path, )
        rects = Rect.Rect.get_rects_from_yolo_json(json_res)
        if len(rects) > 1:
            min_xmin = min(rects[0].xmin, rects[1].xmin)
            max_xmin = max(rects[0].xmin, rects[1].xmin)
            min_xmax = min(rects[0].xmax, rects[1].xmax)
            max_xmax = max(rects[0].xmax, rects[1].xmax)
            per_cent = (min_xmax - max_xmin) / float(max_xmax - min_xmin)
            if per_cent > 0.3:
                if (rects[0].ymax - rects[0].ymin) < (rects[1].ymax - rects[1].ymin):
                    rects.remove(rects[0])
                else:
                    rects.remove(rects[1])
        rects.sort(key = lambda rect: rect.xmin)
        return rects


