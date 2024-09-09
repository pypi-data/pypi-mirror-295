import hashlib
import json
import os
from datetime import datetime

import cv2

import torch

from data.neuro.letters_in_image import Letters_In_Image
from data.result.Class_text import Class_text
from data.result.Class_text_altai import Class_text_altai
from data.result.Label_area import Label_area


class Balka_Text_Recognize_altai_yolo:

    def __init__(self, model_path, yolo_path, prod_coefficients):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        self.model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
        self.prod_coefficients = prod_coefficients
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

    def prepare_cuts(self, image_cuts_2_half_balkas, class_text, has_prod = True):
        result_img_cuts = []
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


    def work_image_cut(self, image_text_areas_2_half_balkas, image_balka_cuts):
        """main_method takes all image_text_areas from image_rama_cut and recognize text"""
        # number
        result_number_img_cuts = []
        result_prod_image_cuts = []
        result_year_image_cuts = []
        if len(image_text_areas_2_half_balkas) == 2:
            seria_left = (len(image_text_areas_2_half_balkas[0].areas[Class_text_altai.seria]) > 0)
            seria_right = (len(image_text_areas_2_half_balkas[1].areas[Class_text_altai.seria]) > 0)
            if (not seria_left) and seria_right:
                number_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.number]
                image_rama_cut = image_balka_cuts[0]
                number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
                for (number_img_cut) in number_image_cuts:
                    result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                pattern_index = 1
            elif seria_left and (not(seria_right)):
                i = 0
                number_image_cuts_2_half_balkas = []
                for image_text_areas in image_text_areas_2_half_balkas:
                    number_image_rects = image_text_areas.areas[Class_text_altai.number]
                    image_rama_cut = image_balka_cuts[i]
                    number_image_cuts_2_half_balkas.append(self.make_cuts(image_rama_cut, number_image_rects))
                    i += 1
                for (number_img_cut) in number_image_cuts_2_half_balkas[0]:
                    result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                for (number_img_cut) in number_image_cuts_2_half_balkas[1]:
                    result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                pattern_index = 0
            else:
                if len(image_text_areas_2_half_balkas[1].areas[Class_text_altai.sran]) > 0:
                    number_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.number]
                    image_rama_cut = image_balka_cuts[0]
                    number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
                    for (number_img_cut) in number_image_cuts:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    pattern_index = 1
                else:
                    i = 0
                    number_image_cuts_2_half_balkas = []
                    for image_text_areas in image_text_areas_2_half_balkas:
                        number_image_rects = image_text_areas.areas[Class_text_altai.number]
                        image_rama_cut = image_balka_cuts[i]
                        number_image_cuts_2_half_balkas.append(self.make_cuts(image_rama_cut, number_image_rects))
                        i += 1
                    for (number_img_cut) in number_image_cuts_2_half_balkas[0]:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    for (number_img_cut) in number_image_cuts_2_half_balkas[1]:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    pattern_index = 0
            prod_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.prod]
            image_rama_cut = image_balka_cuts[0]
            result_prod_image_cuts = self.make_cuts(image_rama_cut, prod_image_rects)
            year_image_rects = image_text_areas_2_half_balkas[1].areas[Class_text_altai.year]
            image_rama_cut = image_balka_cuts[1]
            result_year_image_cuts = self.make_cuts(image_rama_cut, year_image_rects)
        else:
            has_prod = (len(image_text_areas_2_half_balkas[0].areas[Class_text_altai.prod]) > 0)
            has_year = (len(image_text_areas_2_half_balkas[0].areas[Class_text_altai.year]) > 0)
            has_seria = (len(image_text_areas_2_half_balkas[0].areas[Class_text_altai.seria]) > 0)
            has_sran = (len(image_text_areas_2_half_balkas[0].areas[Class_text_altai.sran]) > 0)
            if has_prod:
                if has_seria:
                    number_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.number]
                    image_rama_cut = image_balka_cuts[0]
                    number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
                    for (number_img_cut) in number_image_cuts:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_COUNTERCLOCKWISE))
                    pattern_index = 0
                    prod_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.prod]
                    image_rama_cut = image_balka_cuts[0]
                    result_prod_image_cuts = self.make_cuts(image_rama_cut, prod_image_rects)
                else:
                    number_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.number]
                    image_rama_cut = image_balka_cuts[0]
                    number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
                    for (number_img_cut) in number_image_cuts:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    pattern_index = 1
                    prod_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.prod]
                    image_rama_cut = image_balka_cuts[0]
                    result_prod_image_cuts = self.make_cuts(image_rama_cut, prod_image_rects)
            else:
                if has_seria:
                    year_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.year]
                    image_rama_cut = image_balka_cuts[0]
                    result_year_image_cuts = self.make_cuts(image_rama_cut, year_image_rects)
                    pattern_index = 1
                else:
                    number_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.number]
                    image_rama_cut = image_balka_cuts[0]
                    number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
                    for (number_img_cut) in number_image_cuts:
                        result_number_img_cuts.append(cv2.rotate(number_img_cut, cv2.ROTATE_90_CLOCKWISE))
                    pattern_index = 0
                    year_image_rects = image_text_areas_2_half_balkas[0].areas[Class_text_altai.year]
                    image_rama_cut = image_balka_cuts[0]
                    result_year_image_cuts = self.make_cuts(image_rama_cut, year_image_rects)
        p_c = self.prod_coefficients[pattern_index]
        #  for debug - comment in production
        # i = 0
        # for result_number_img_cut in result_number_img_cuts:
        #     cv2.namedWindow('number'+str(i), cv2.WINDOW_AUTOSIZE)
        #     cv2.imshow('number'+str(i), result_number_img_cut)
        #     i+=1
        # i = 0
        # for result_prod_image_cut in result_prod_image_cuts:
        #     cv2.namedWindow('prod' + str(i), cv2.WINDOW_AUTOSIZE)
        #     cv2.imshow('prod' + str(i), result_prod_image_cut)
        #     i+=1
        # i = 0
        # for result_year_image_cut in result_year_image_cuts:
        #     cv2.namedWindow('year' + str(i), cv2.WINDOW_AUTOSIZE)
        #     cv2.imshow('year' + str(i), result_year_image_cut)
        #     i += 1
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        (number, number_conf) = self.work_image_cuts(result_number_img_cuts,
                                                     p_c.number_coefficients.length,
                                                     p_c.number_coefficients.height,
                                                     p_c.number_coefficients.width
                                                     )
        (prod, prod_conf) = self.work_image_cuts(result_prod_image_cuts,
                                                     p_c.prod_coefficients.length,
                                                     p_c.prod_coefficients.height,
                                                     p_c.prod_coefficients.width
                                                     )
        (year, year_conf) = self.work_image_cuts(result_year_image_cuts,
                                                     p_c.year_coefficients.length,
                                                     p_c.year_coefficients.height,
                                                     p_c.year_coefficients.width
                                                     )
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
        
