# import os
#
# import cv2
#
from danila.danila_v11 import Danila_v11


"""main module for user"""


class Danila:
    """main class for user"""
    def __init__(self, local, yolov5_dir, detail_classify_version = 1,
                 rama_detect_version = 1, rama_classify_version = 1, rama_text_detect_version = 1, rama_text_recognize_version = 1,
                 vagon_text_detect_version = 1, vagon_text_recognize_version = 1,
                 balka_detect_version = 1, balka_classify_version = 1, balka_text_detect_version = 1, balka_text_recognize_version = 1):
        self.danila = Danila_v11(local, yolov5_dir, detail_classify_version,
                 rama_detect_version, rama_classify_version, rama_text_detect_version, rama_text_recognize_version,
                 vagon_text_detect_version, vagon_text_recognize_version,
                 balka_detect_version, balka_classify_version, balka_text_detect_version, balka_text_recognize_version)
    # returns string - class of rama using CNN network
    # img - openCV frame

    def detail_classify(self, img):
        return self.danila.detail_classify(img)

    def detail_text_detect(self, img):
        return self.danila.detail_text_detect(img)

    def detail_text_recognize(self, img):
        return self.danila.detail_text_recognize(img)

    def rama_classify(self, img):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        return self.danila.rama_classify(img)

    # returns openCV frame with rama from openCV frame\
    # def rama_detect(self, img, size = 256):
    #     """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
    #     return self.danila.rama_detect(img, size)
    #
    # # returns openCV image with cut_rama
    # def rama_cut(self, img, size = 256):
    #     """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
    #     return self.danila.rama_cut(img, size)

    #
    # returns openCV cut rama with drawn text areas
    def rama_text_detect_cut(self, img):
        """returns openCV cut rama with drawn text areas"""
        return self.danila.rama_text_detect_cut(img)

    # returns openCV img with drawn text areas
    # def rama_text_detect(self, img, size = 256):
    #     """returns openCV img with drawn text areas"""
    #     return self.danila.text_detect(img, size)
    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def rama_text_recognize(self, img):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        return self.danila.rama_text_recognize(img)

    # returns openCV img with drawn number areas
    def vagon_number_detect(self, img):
        """returns openCV img with drawn number areas"""
        return self.danila.vagon_number_detect(img)

    def vagon_number_recognize(self, img):
        return self.danila.vagon_number_recognize(img)


    def balka_classify(self, img):
        return self.danila.balka_classify(img)

    def balka_text_detect(self, img):
        return self.danila.balka_text_detect(img)

    def balka_text_recognize(self, img):
        return self.danila.balka_text_recognize(img)