from data.result.Class_text import Class_text
from data.result.Class_text_altai import Class_text_altai
from data.result.Rect import Rect


class Text_area_altai:

    def __init__(self, dict_text_area):
        self.class_im = Class_text_altai(dict_text_area['class'])
        self.rect = Rect(
                            xmin = int(float(dict_text_area['xmin'])),
                            xmax = int(float(dict_text_area['xmax'])),
                            ymin = int(float(dict_text_area['ymin'])),
                            ymax = int(float(dict_text_area['ymax']))
        )



