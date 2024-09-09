import hashlib
import json
import os
import zipfile
from datetime import datetime

import cv2
import requests
from urllib.parse import urlencode
import torch

from data.neuro.letters_in_image import Letters_In_Image
from data.result import balka_prod
from data.result.Class_text import Class_text
from data.result.Label_area import Label_area
class Balka_text_cut_recognize_params:
    def __init__(self, length, height, width):
        self.length = length
        self.height = height
        self.width = width

class Balka_text_recognize_params:
    def __init__(self, number_params, prod_params, year_params):
        self.number_params = number_params
        self.prod_params = prod_params
        self.year_params = year_params

class Balka_Text_Recognize_yolo:

    def __init__(self, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

        # for every text_class try to recognize text from all areas of text_class, number_params is depends on class and prod, returns string

    def work_image_cuts(self, number_image_cuts, l, h, w):
        """for every text_class try to recognize text from all areas of text_class, number_params is depends on class and prod, returns string """
        (str,conf) = ('', 0.0)
        for number_image_cut in number_image_cuts:
            # cv2.imwrite('data/neuro_classes/cut.jpg', number_image_cut)
            (cur_str, cur_conf) = self.work_img_word(number_image_cut, l, h, w)
            if len(cur_str) == l:
                if cur_conf > conf:
                    (str, conf) = (cur_str, cur_conf)
            elif len(cur_str) > len(str):
                (str, conf) = (cur_str, cur_conf)
            elif (len(cur_str) == len(str)) & (cur_conf > conf):
                (str, conf) = (cur_str, cur_conf)
        return (str, round(conf,2))

        # main_method takes all image_text_areas from image_rama_cut and recognize text

    def prepare_cuts(self, _balka_prod, image_cuts_2_half_balkas, class_text, has_prod = True):
        result_img_cuts = []
        if (_balka_prod == balka_prod.Balka_Prod.altai):
            if class_text == Class_text.number:
                if len(image_cuts_2_half_balkas) == 2:
                    for (number_img_cut) in image_cuts_2_half_balkas[0]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    for (number_img_cut) in image_cuts_2_half_balkas[1]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    return result_img_cuts
                elif len(image_cuts_2_half_balkas) == 1:
                    if has_prod:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    else:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    return result_img_cuts
                else:
                    return result_img_cuts
            elif class_text == Class_text.prod:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
            elif class_text == Class_text.year:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
        elif (_balka_prod == balka_prod.Balka_Prod.begickaya):
            if class_text == Class_text.number:
                if len(image_cuts_2_half_balkas) == 2:
                    for (number_img_cut) in image_cuts_2_half_balkas[0]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    for (number_img_cut) in image_cuts_2_half_balkas[1]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                elif len(image_cuts_2_half_balkas) == 1:
                    if has_prod:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    else:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                else:
                    return result_img_cuts
            elif class_text == Class_text.prod:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
            elif class_text == Class_text.year:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
        elif (_balka_prod == balka_prod.Balka_Prod.promlit):
            if class_text == Class_text.number:
                if len(image_cuts_2_half_balkas) == 2:
                    for (number_img_cut) in image_cuts_2_half_balkas[0]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    for (number_img_cut) in image_cuts_2_half_balkas[1]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                elif len(image_cuts_2_half_balkas) == 1:
                    if has_prod:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    else:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    return result_img_cuts
                else:
                    return result_img_cuts
            elif class_text == Class_text.prod:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
            elif class_text == Class_text.year:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
        elif (_balka_prod == balka_prod.Balka_Prod.ruzhimmash):
            if class_text == Class_text.number:
                if len(image_cuts_2_half_balkas) == 2:
                    for (number_img_cut) in image_cuts_2_half_balkas[0]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    for (number_img_cut) in image_cuts_2_half_balkas[1]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                elif len(image_cuts_2_half_balkas) == 1:
                    if has_prod:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    else:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                else:
                    return result_img_cuts
            elif class_text == Class_text.prod:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
            elif class_text == Class_text.year:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(image_cut)
                return result_img_cuts
        elif (_balka_prod == balka_prod.Balka_Prod.tihvin):
            if class_text == Class_text.number:
                if len(image_cuts_2_half_balkas) == 2:
                    for (number_img_cut) in image_cuts_2_half_balkas[0]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    for (number_img_cut) in image_cuts_2_half_balkas[1]:
                        result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                elif len(image_cuts_2_half_balkas) == 1:
                    if has_prod:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    else:
                        for (number_img_cut) in image_cuts_2_half_balkas[0]:
                            result_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    return result_img_cuts
                else:
                    return result_img_cuts
            elif class_text == Class_text.prod:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(cv2.rotate(image_cut, cv2.ROTATE_90_CLOCKWISE))
                return result_img_cuts
            elif class_text == Class_text.year:
                for image_cuts in image_cuts_2_half_balkas:
                    for image_cut in image_cuts:
                        result_img_cuts.append(cv2.rotate(image_cut, cv2.ROTATE_90_CLOCKWISE))
                return result_img_cuts

    def work_image_cut(self, _balka_prod, image_text_areas_2_half_balkas, image_balka_cuts,
                       number_l, number_h, number_w, prod_l, prod_h, prod_w, year_l, year_h, year_w):
        """main_method takes all image_text_areas from image_rama_cut and recognize text"""
        i = 0
        number_image_cuts_2_half_balkas = []
        for image_text_areas in image_text_areas_2_half_balkas:
            number_image_rects = image_text_areas.areas[Class_text.number]
            image_rama_cut = image_balka_cuts[i]
            number_image_cuts_2_half_balkas.append(self.make_cuts(image_rama_cut, number_image_rects))
            i += 1
        has_prod = True
        if len(image_text_areas_2_half_balkas) == 1:
            has_prod = (len(image_text_areas_2_half_balkas[0].areas[Class_text.prod]) > 0)
        number_image_cuts = self.prepare_cuts(_balka_prod, number_image_cuts_2_half_balkas, Class_text.number, has_prod)
        (number, number_conf) = self.work_image_cuts(number_image_cuts, number_l, number_h, number_w)

        i = 0
        prod_image_cuts_2_half_balkas = []
        for image_text_areas in image_text_areas_2_half_balkas:
            prod_image_rects = image_text_areas.areas[Class_text.prod]
            image_rama_cut = image_balka_cuts[i]
            prod_image_cuts_2_half_balkas.append(self.make_cuts(image_rama_cut, prod_image_rects))
            i += 1
        has_prod = True
        prod_image_cuts = self.prepare_cuts(_balka_prod, prod_image_cuts_2_half_balkas, Class_text.prod, has_prod)
        (prod, prod_conf) = self.work_image_cuts(prod_image_cuts, prod_l, prod_h, prod_w)

        i = 0
        year_image_cuts_2_half_balkas = []
        for image_text_areas in image_text_areas_2_half_balkas:
            year_image_rects = image_text_areas.areas[Class_text.year]
            image_rama_cut = image_balka_cuts[i]
            year_image_cuts_2_half_balkas.append(self.make_cuts(image_rama_cut, year_image_rects))
            i += 1
        has_prod = True
        year_image_cuts = self.prepare_cuts(_balka_prod, year_image_cuts_2_half_balkas, Class_text.year, has_prod)
        (year, year_conf) = self.work_image_cuts(year_image_cuts, year_l, year_h, year_w)

        label_area = Label_area()
        label_area.labels[Class_text.number] = (number, number_conf)
        label_area.labels[Class_text.prod] = (prod, prod_conf)
        label_area.labels[Class_text.year] = (year, year_conf)
        return label_area

    def work_img_word(self, number_image_cut, l, number_h, number_w):
        h, w = number_image_cut.shape[:2]
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_cut_path = 'cut_text_img' + hash_str + '.jpg'
        cv2.imwrite(img_cut_path, number_image_cut)
        self.model.max_det = l
        results = self.model(img_cut_path, size=(number_h, number_w))
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
        img_letters.sort_letters()
        img_letters.delete_intersections()
        os.remove(img_cut_path)
        return img_letters.make_word(), img_letters.get_avg_conf()

    # cut text_areas imgs for each Rect from rect_array returns openCv imgs list
    def make_cuts(self, img_balka_cut, rect_array):
        """cut text_areas imgs for each Rect from rect_array returns openCv imgs list"""
        number_image_cuts = []
        for rect in rect_array:
            number_image_cuts.append(img_balka_cut[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        return number_image_cuts
        
