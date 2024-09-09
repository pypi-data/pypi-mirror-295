import hashlib
import os
from datetime import datetime

import cv2

from data.neuro.Balka_detect_class import Balka_detect_class
from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.Rama_text_detect_class import Rama_text_detect_class
from data.neuro.balka_text_detect_class import Balka_text_detect_class
from data.neuro.local_models import *
from data.neuro.models import *
from data.result import Rama_prod, balka_prod


class Danila_balka_text_detect_base:
    def __init__(self, local, yolov5_dir, balka_detect_version, balka_text_detect_version):
        if local:
            if (balka_detect_version == 1) & (balka_text_detect_version == 1):

                self.balka_detect_objects = {
                     balka_prod.Balka_Prod.altai: None,
                     balka_prod.Balka_Prod.begickaya: None,
                     balka_prod.Balka_Prod.promlit: None,
                     balka_prod.Balka_Prod.ruzhimmash: None,
                     balka_prod.Balka_Prod.tihvin: None
                }

                print('reading and loading - BALKA_ALTAI_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.altai] = Balka_detect_class(local, LOCAL_BALKA_ALTAI_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_BEGICKAYA_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.begickaya] = Balka_detect_class(local, LOCAL_BALKA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_PROMLIT_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.promlit] = Balka_detect_class(local, LOCAL_BALKA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_RUZHIMMASH_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.ruzhimmash] = Balka_detect_class(local, LOCAL_BALKA_RUZHIMMASH_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_TIHVIN_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.tihvin] = Balka_detect_class(local, LOCAL_BALKA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)


                self.balka_text_detect_objects = {
                    balka_prod.Balka_Prod.altai: None,
                    balka_prod.Balka_Prod.begickaya: None,
                    balka_prod.Balka_Prod.promlit: None,
                    balka_prod.Balka_Prod.ruzhimmash: None,
                    balka_prod.Balka_Prod.tihvin: None
                }

                print('reading and loading - BALKA_ALTAI_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.altai] = Balka_text_detect_class(
                    local, LOCAL_BALKA_ALTAI_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.altai)

                print('reading and loading - BALKA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.begickaya] = Balka_text_detect_class(
                    local, LOCAL_BALKA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.begickaya)

                print('reading and loading - BALKA_PROMLIT_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.promlit] = Balka_text_detect_class(
                    local, LOCAL_BALKA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.promlit)

                print('reading and loading - BALKA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.ruzhimmash] = Balka_text_detect_class(
                    local, LOCAL_BALKA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.ruzhimmash)

                print('reading and loading - BALKA_TIHVIN_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.tihvin] = Balka_text_detect_class(
                    local, LOCAL_BALKA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir, balka_prod.Balka_Prod.tihvin)
        else:
            if (balka_detect_version == 1) & (balka_text_detect_version == 1):
                self.balka_detect_objects = {
                    balka_prod.Balka_Prod.altai: None,
                    balka_prod.Balka_Prod.begickaya: None,
                    balka_prod.Balka_Prod.promlit: None,
                    balka_prod.Balka_Prod.ruzhimmash: None,
                    balka_prod.Balka_Prod.tihvin: None
                }

                print('reading and loading - BALKA_ALTAI_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.altai] = Balka_detect_class(
                    local, BALKA_ALTAI_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_BEGICKAYA_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.begickaya] = Balka_detect_class(
                    local, BALKA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_PROMLIT_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.promlit] = Balka_detect_class(
                    local, BALKA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_RUZHIMMASH_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.ruzhimmash] = Balka_detect_class(
                    local, BALKA_RUZHIMMASH_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - BALKA_TIHVIN_DETECT_MODEL')
                self.balka_detect_objects[balka_prod.Balka_Prod.tihvin] = Balka_detect_class(
                    local, BALKA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                self.balka_text_detect_objects = {
                    balka_prod.Balka_Prod.altai: None,
                    balka_prod.Balka_Prod.begickaya: None,
                    balka_prod.Balka_Prod.promlit: None,
                    balka_prod.Balka_Prod.ruzhimmash: None,
                    balka_prod.Balka_Prod.tihvin: None
                }

                print('reading and loading - BALKA_ALTAI_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.altai] = Balka_text_detect_class(
                    local, BALKA_ALTAI_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.altai)

                print('reading and loading - BALKA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.begickaya] = Balka_text_detect_class(
                    local, BALKA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.begickaya)

                print('reading and loading - BALKA_PROMLIT_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.promlit] = Balka_text_detect_class(
                    local, BALKA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.promlit)

                print('reading and loading - BALKA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.ruzhimmash] = Balka_text_detect_class(
                    local, BALKA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir, balka_prod.Balka_Prod.ruzhimmash)

                print('reading and loading - BALKA_TIHVIN_TEXT_DETECT_MODEL')
                self.balka_text_detect_objects[balka_prod.Balka_Prod.tihvin] = Balka_text_detect_class(
                    local, BALKA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir, balka_prod.Balka_Prod.tihvin)

    def balka_text_detect(self, img, balka_prod):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_balka' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rects = self.balka_detect_objects[balka_prod].balka_detect(initial_image_path)
        if rects == []:
            os.remove(initial_image_path)
            return img
        imgs = []
        for rect in rects:
            imgs.append(img[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        image_text_areas_half_balkas = self.balka_text_detect_objects[balka_prod].balka_text_detect(imgs)
        images_drawn_text_areas = self.balka_text_detect_objects[balka_prod].draw_text_areas_in_opencv(
            image_text_areas_half_balkas, imgs)
        if len(images_drawn_text_areas) == 1:
            new_img = images_drawn_text_areas[0]
        else:
            h0, w0 = images_drawn_text_areas[0].shape[:2]
            h1, w1 = images_drawn_text_areas[1].shape[:2]
            dsize = (w0 + w1, max(h0,h1))
            new_img = cv2.resize(images_drawn_text_areas[0],dsize)
            left_image = cv2.resize(images_drawn_text_areas[0], ( w0, max(h0,h1)))
            right_image = cv2.resize(images_drawn_text_areas[1], ( w1, max(h0,h1)))
            for i in range(max(h0,h1)):
                for j in range(w0):
                    new_img[i,j] = left_image[i,j]
                for k in range(w0,w0+w1):
                    new_img[i,k] = right_image[i,k - w0]
        os.remove(initial_image_path)
        return new_img

    def balka_text_detect_cuts(self, img, balka_prod):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_balka' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rects = self.balka_detect_objects[balka_prod].balka_detect(initial_image_path)
        if rects == []:
            os.remove(initial_image_path)
            return [], []
        imgs = []
        for rect in rects:
            imgs.append(img[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        image_text_areas_half_balkas = self.balka_text_detect_objects[balka_prod].balka_text_detect(imgs)
        os.remove(initial_image_path)
        return imgs, image_text_areas_half_balkas