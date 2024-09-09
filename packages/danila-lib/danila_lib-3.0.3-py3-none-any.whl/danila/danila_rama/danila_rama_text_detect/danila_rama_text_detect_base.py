import hashlib
import os
from datetime import datetime

import cv2

from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.Rama_text_detect_class import Rama_text_detect_class
from data.neuro.local_models import *
from data.neuro.models import *
from data.result import Rama_prod


class Danila_rama_text_detect_base:
    def __init__(self, local, yolov5_dir, rama_detect_version, rama_text_detect_version):

        if local:
            if (rama_detect_version == 1) & (rama_text_detect_version == 1):

                self.rama_detect_objects = {
                     Rama_prod.Rama_Prod.altai: None,
                     Rama_prod.Rama_Prod.balakovo: None,
                     Rama_prod.Rama_Prod.begickaya: None,
                     Rama_prod.Rama_Prod.promlit: None,
                     Rama_prod.Rama_Prod.ruzhimmash: None,
                     Rama_prod.Rama_Prod.tihvin: None,
                     Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, LOCAL_RAMA_ALTAI_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(local, LOCAL_RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(local, LOCAL_RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(local, LOCAL_RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(local, LOCAL_RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(local, LOCAL_RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, LOCAL_RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(local, LOCAL_RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(local, LOCAL_RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                                                                                           yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(local, LOCAL_RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                                                                                            yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(local, LOCAL_RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, LOCAL_RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(local, LOCAL_RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                                                                                         yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, LOCAL_RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 2) & (rama_text_detect_version == 2):

                self.rama_detect_objects = {
                     Rama_prod.Rama_Prod.altai: None,
                     Rama_prod.Rama_Prod.balakovo: None,
                     Rama_prod.Rama_Prod.begickaya: None,
                     Rama_prod.Rama_Prod.promlit: None,
                     Rama_prod.Rama_Prod.ruzhimmash: None,
                     Rama_prod.Rama_Prod.tihvin: None,
                     Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, LOCAL_RAMA_ALTAI_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(local, LOCAL_RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(local, LOCAL_RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(local, LOCAL_RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(local, LOCAL_RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(local, LOCAL_RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, LOCAL_RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(local, LOCAL_RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(local, LOCAL_RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                                                                                           yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(local, LOCAL_RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                                                                                            yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(local, LOCAL_RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, LOCAL_RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(local, LOCAL_RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                                                                                         yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, LOCAL_RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 3) & (rama_text_detect_version == 3):

                self.rama_detect_objects = {
                     Rama_prod.Rama_Prod.altai: None,
                     Rama_prod.Rama_Prod.balakovo: None,
                     Rama_prod.Rama_Prod.begickaya: None,
                     Rama_prod.Rama_Prod.promlit: None,
                     Rama_prod.Rama_Prod.ruzhimmash: None,
                     Rama_prod.Rama_Prod.tihvin: None,
                     Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, LOCAL_RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(local, LOCAL_RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(local, LOCAL_RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(local, LOCAL_RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(local, LOCAL_RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(local, LOCAL_RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, LOCAL_RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(local, LOCAL_RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(local, LOCAL_RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                                                                                           yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(local, LOCAL_RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                                                                                            yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(local, LOCAL_RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, LOCAL_RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(local, LOCAL_RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                                                                                         yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, LOCAL_RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 4) & (rama_text_detect_version == 4):

                self.rama_detect_objects = {
                     Rama_prod.Rama_Prod.altai: None,
                     Rama_prod.Rama_Prod.balakovo: None,
                     Rama_prod.Rama_Prod.begickaya: None,
                     Rama_prod.Rama_Prod.promlit: None,
                     Rama_prod.Rama_Prod.ruzhimmash: None,
                     Rama_prod.Rama_Prod.tihvin: None,
                     Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, LOCAL_RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(local, LOCAL_RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(local, LOCAL_RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(local, LOCAL_RAMA_PROMLIT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(local, LOCAL_RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(local, LOCAL_RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, LOCAL_RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(local, LOCAL_RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(local, LOCAL_RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                                                                                           yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(local, LOCAL_RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                                                                                            yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(local, LOCAL_RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS_2,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, LOCAL_RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(local, LOCAL_RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                                                                                         yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, LOCAL_RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 5) & (rama_text_detect_version == 4):

                self.rama_detect_objects = {
                     Rama_prod.Rama_Prod.altai: None,
                     Rama_prod.Rama_Prod.balakovo: None,
                     Rama_prod.Rama_Prod.begickaya: None,
                     Rama_prod.Rama_Prod.promlit: None,
                     Rama_prod.Rama_Prod.ruzhimmash: None,
                     Rama_prod.Rama_Prod.tihvin: None,
                     Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, LOCAL_RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(local, LOCAL_RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(local, LOCAL_RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(local, LOCAL_RAMA_PROMLIT_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(local, LOCAL_RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(local, LOCAL_RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                                                                                          yolov5_dir, True)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, LOCAL_RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(local, LOCAL_RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(local, LOCAL_RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                                                                                           yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(local, LOCAL_RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                                                                                            yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(local, LOCAL_RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS_2,
                                                                                          yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, LOCAL_RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(local, LOCAL_RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                                                                                         yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, LOCAL_RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
        else:
            if (rama_detect_version == 1) & (rama_text_detect_version == 1):

                self.rama_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, RAMA_ALTAI_DETECT_MODEL_ADDRESS,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(
                    local, RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(
                    local, RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(
                    local, RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(
                    local, RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(
                    local, RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(
                    local, RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(
                    local, RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(
                    local, RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(
                    local, RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(
                    local, RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 2) & (rama_text_detect_version == 2):

                self.rama_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(local, RAMA_ALTAI_DETECT_MODEL_ADDRESS,
                                                                                        yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(
                    local, RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(
                    local, RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(
                    local, RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(
                    local, RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(
                    local, RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(
                    local, RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(
                    local, RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(
                    local, RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(
                    local, RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(
                    local, RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 3) & (rama_text_detect_version == 3):

                self.rama_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(
                    local, RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(
                    local, RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(
                    local, RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(
                    local, RAMA_PROMLIT_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(
                    local, RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(
                    local, RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(
                    local, RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                    yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(
                    local, RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(
                    local, RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(
                    local, RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(
                    local, RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 4) & (rama_text_detect_version == 4):

                self.rama_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(
                    local, RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(
                    local, RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(
                    local, RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(
                    local, RAMA_PROMLIT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(
                    local, RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(
                    local, RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(
                    local, RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                    yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(
                    local, RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(
                    local, RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(
                    local, RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS_2,
                    yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(
                    local, RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)
            elif (rama_detect_version == 5) & (rama_text_detect_version == 4):

                self.rama_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_detect_class(
                    local, RAMA_ALTAI_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_BALAKOVO_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_detect_class(
                    local, RAMA_BALAKOVO_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                print('reading and loading - RAMA_BEGICKAYA_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_detect_class(
                    local, RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                print('reading and loading - RAMA_PROMLIT_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_detect_class(
                    local, RAMA_PROMLIT_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_RUZHIMMASH_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_detect_class(
                    local, RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS_2, yolov5_dir, True)

                print('reading and loading - RAMA_TIHVIN_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_detect_class(
                    local, RAMA_TIHVIN_DETECT_MODEL_ADDRESS,
                    yolov5_dir, True)

                print('reading and loading - RAMA_URALVAGON_DETECT_MODEL')
                self.rama_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_detect_class(
                    local, RAMA_URALVAGON_DETECT_MODEL_ADDRESS, yolov5_dir, True)

                self.rama_text_detect_objects = {
                    Rama_prod.Rama_Prod.altai: None,
                    Rama_prod.Rama_Prod.balakovo: None,
                    Rama_prod.Rama_Prod.begickaya: None,
                    Rama_prod.Rama_Prod.promlit: None,
                    Rama_prod.Rama_Prod.ruzhimmash: None,
                    Rama_prod.Rama_Prod.tihvin: None,
                    Rama_prod.Rama_Prod.uralvagon: None
                }

                print('reading and loading - RAMA_ALTAI_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.altai] = Rama_text_detect_class(
                    local, RAMA_ALTAI_TEXT_DETECT_MODEL_ADDRESS_2,
                    yolov5_dir)

                print('reading and loading - RAMA_BALAKOVO_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.balakovo] = Rama_text_detect_class(
                    local, RAMA_BALAKOVO_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_BEGICKAYA_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.begickaya] = Rama_text_detect_class(
                    local, RAMA_BEGICKAYA_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_PROMLIT_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.promlit] = Rama_text_detect_class(
                    local, RAMA_PROMLIT_TEXT_DETECT_MODEL_ADDRESS_2,
                    yolov5_dir)

                print('reading and loading - RAMA_RUZHIMMASH_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.ruzhimmash] = Rama_text_detect_class(
                    local, RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS_2, yolov5_dir)

                print('reading and loading - RAMA_TIHVIN_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.tihvin] = Rama_text_detect_class(
                    local, RAMA_TIHVIN_TEXT_DETECT_MODEL_ADDRESS,
                    yolov5_dir)

                print('reading and loading - RAMA_URALVAGON_TEXT_DETECT_MODEL')
                self.rama_text_detect_objects[Rama_prod.Rama_Prod.uralvagon] = Rama_text_detect_class(
                    local, RAMA_URALVAGON_TEXT_DETECT_MODEL_ADDRESS, yolov5_dir)

    def rama_text_detect(self, img, rama_prod):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rect = self.rama_detect_objects[rama_prod].rama_detect(initial_image_path)
        if rect is None:
            image_text_areas = self.rama_text_detect_objects[rama_prod].text_detect(initial_image_path)
            image_drawn_text_areas = self.rama_text_detect_objects[rama_prod].draw_text_areas_in_opencv(
                image_text_areas, img)
            os.remove(initial_image_path)
            return image_drawn_text_areas
        img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_cut_path = 'cut_img' + hash_str + '.jpg'
        cv2.imwrite(img_cut_path, img_cut)
        image_text_areas = self.rama_text_detect_objects[rama_prod].text_detect(img_cut_path)
        image_drawn_text_areas = self.rama_text_detect_objects[rama_prod].draw_text_areas_in_opencv(
            image_text_areas, img_cut)
        os.remove(initial_image_path)
        os.remove(img_cut_path)
        return image_drawn_text_areas

    def rama_text_detect_cuts(self, img, rama_prod):
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, img)
        rect = self.rama_detect_objects[rama_prod].rama_detect(initial_image_path)
        if rect is None:
            image_text_areas = self.rama_text_detect_objects[rama_prod].text_detect(initial_image_path)
            os.remove(initial_image_path)
            return img, image_text_areas
        img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        img_cut_path = 'cut_img' + hash_str + '.jpg'
        cv2.imwrite(img_cut_path, img_cut)
        image_text_areas = self.rama_text_detect_objects[rama_prod].text_detect(img_cut_path)
        os.remove(initial_image_path)
        os.remove(img_cut_path)
        return img_cut, image_text_areas