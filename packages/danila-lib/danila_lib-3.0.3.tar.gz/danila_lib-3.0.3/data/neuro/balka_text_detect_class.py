import hashlib
import json
import os
from datetime import datetime

import cv2
import torch
import zipfile
import requests
from urllib.parse import urlencode

from data.neuro.letters_in_image import Letters_In_Image
from data.result.Class_text import Class_text
from data.result.Image_text_areas import Image_text_areas
from data.result.Text_area import Text_area
from data.result.balka_prod import Balka_Prod

"""module for detecting text in rama"""
class Balka_text_detect_class:
    """class for detecting text in rama"""
    # reads yolov5 taught model from yandex-disk and includes it in class example
    def __init__(self, model_path, yolo_path, balka_prod):
        self.balka_prod = balka_prod
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

    # find text areas on img from img_path with yolov5, returns yolojson
    def work_img(self, img_path):
        """find text areas on img from img_path with yolov5, returns yolojson"""

        results = self.model([img_path], size=256)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        return res2
    # find text areas on img from img_path with yolov5, returns dict with rects for each text class
    def text_detect(self, img_path):
        """find text areas on img from img_path with yolov5, returns dict with rects for each text class"""
        json_res = self.work_img(img_path)
        image_text_areas = Image_text_areas()
        image_text_areas_list = Letters_In_Image.get_letters_in_image_from_yolo_json(json_res)
        image_text_areas_list.sort_letters()
        image_text_areas_list.delete_intersections()
        json_res_1 = []
        for image_text_areas_list_el in image_text_areas_list.letters:
            dict = {}
            dict['confidence'] = image_text_areas_list_el.confidence
            dict['xmin'] = image_text_areas_list_el.rect.xmin
            dict['xmax'] = image_text_areas_list_el.rect.xmax
            dict['ymin'] = image_text_areas_list_el.rect.ymin
            dict['ymax'] = image_text_areas_list_el.rect.ymax
            if image_text_areas_list_el.letter == 'number':
                dict['class'] = 0
            elif image_text_areas_list_el.letter == 'prod':
                dict['class'] = 1
            elif image_text_areas_list_el.letter == 'text':
                dict['class'] = 2
            elif image_text_areas_list_el.letter == 'year':
                dict['class'] = 3
            json_res_1.append(dict)
        for text_area_json in json_res_1:
            if text_area_json['confidence']>0.25:
                text_area = Text_area(text_area_json)
                image_text_areas.add_area(text_area)
        image_text_areas.correct_intersections()
        return image_text_areas

    def balka_text_detect(self, imgs):
        img_text_areas_in_two_balkas = []
        for img in imgs:
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_balka_' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, img)
            img_text_areas = self.text_detect(img_cut_path)
            img_text_areas_in_two_balkas.append(img_text_areas)
            os.remove(img_cut_path)
        if len(img_text_areas_in_two_balkas) > 1:
            img_text_areas_in_two_balkas = self.work_text_areas_for_prod(img_text_areas_in_two_balkas[0], img_text_areas_in_two_balkas[1])
        return img_text_areas_in_two_balkas

    # draw img_text_areas on img, returns opencv img
    def draw_text_areas_in_opencv(self, img_text_areas_in_two_balkas, imgs):
        """draw img_text_areas on img, returns opencv img"""
        colors = [(0,0,255), (0,255,0), (255,255,255), (255,0,0)]
        i = 0
        for image_text_areas in img_text_areas_in_two_balkas:
            for class_im in image_text_areas.areas:
                for rect in image_text_areas.areas[class_im]:
                    cv2.rectangle(imgs[i], (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), color=colors[class_im.value], thickness=2)
                    cv2.putText(imgs[i], class_im.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=colors[class_im.value], thickness=1)
            i += 1
        return imgs

    def work_text_areas_for_prod(self, left_half_balka, right_half_balka):
        if self.balka_prod == Balka_Prod.altai:
            return self.work_text_areas_for_altai(left_half_balka, right_half_balka)
        elif self.balka_prod == Balka_Prod.begickaya:
            return self.work_text_areas_for_begickaya(left_half_balka, right_half_balka)
        elif self.balka_prod == Balka_Prod.promlit:
            return self.work_text_areas_for_promlit(left_half_balka, right_half_balka)
        elif self.balka_prod == Balka_Prod.ruzhimmash:
            return self.work_text_areas_for_ruzhimmash(left_half_balka, right_half_balka)
        elif self.balka_prod == Balka_Prod.tihvin:
            return self.work_text_areas_for_tihvin(left_half_balka, right_half_balka)
    def work_text_areas_for_altai(self, left_half_balka, right_half_balka):
        if len(left_half_balka.areas[Class_text.year]) > 0:
            left_half_balka.areas[Class_text.year] = []
        if len(right_half_balka.areas[Class_text.prod]) > 0:
            right_half_balka.areas[Class_text.prod] = []
        return [left_half_balka, right_half_balka]

    def work_text_areas_for_begickaya(self, left_half_balka, right_half_balka):
        if len(right_half_balka.areas[Class_text.year]) > 0:
            right_half_balka.areas[Class_text.year] = []
        if len(right_half_balka.areas[Class_text.prod]) > 0:
            right_half_balka.areas[Class_text.prod] = []
        return [left_half_balka, right_half_balka]

    def work_text_areas_for_promlit(self, left_half_balka, right_half_balka):
        if len(right_half_balka.areas[Class_text.year]) > 0:
            right_half_balka.areas[Class_text.year] = []
        if len(left_half_balka.areas[Class_text.prod]) > 0:
            left_half_balka.areas[Class_text.prod] = []
        return [left_half_balka, right_half_balka]

    def work_text_areas_for_ruzhimmash(self, left_half_balka, right_half_balka):
        if len(right_half_balka.areas[Class_text.year]) > 0:
            right_half_balka.areas[Class_text.year] = []
        if len(right_half_balka.areas[Class_text.prod]) > 0:
            right_half_balka.areas[Class_text.prod] = []
        return [left_half_balka, right_half_balka]

    def work_text_areas_for_tihvin(self, left_half_balka, right_half_balka):
        if len(right_half_balka.areas[Class_text.year]) > 0:
            right_half_balka.areas[Class_text.year] = []
        if len(right_half_balka.areas[Class_text.prod]) > 0:
            right_half_balka.areas[Class_text.prod] = []
        return [left_half_balka, right_half_balka]

