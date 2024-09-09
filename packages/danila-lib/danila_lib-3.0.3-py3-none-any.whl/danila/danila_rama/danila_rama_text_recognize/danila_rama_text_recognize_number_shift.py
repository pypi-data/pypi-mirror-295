from data.result.Class_text import Class_text
from data.result.Rect import Rect


class Danila_rama_text_recognize_number_shift:
    def __init__(self, danila_rama_text_recognize):
        self.danila_rama_text_recognize = danila_rama_text_recognize

    def get_number_length(self, rama_prod):
        return self.danila_rama_text_recognize.get_number_length(rama_prod)

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        res_labels = self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, image_text_areas)
        (number_text, _) = res_labels['number']
        if len(number_text) == self.danila_rama_text_recognize.get_number_length(rama_prod):
            return res_labels
        else:
            number_image_text_areas = image_text_areas.areas[Class_text.number]
            image_text_areas_min = []
            image_text_areas_max = []
            for number_image_text_area in number_image_text_areas:
                w = number_image_text_area.xmax - number_image_text_area.xmin
                if (number_image_text_area.xmin - (w // 2)) < 0:
                    new_xmin = 0
                else:
                    new_xmin = number_image_text_area.xmin - (w // 2)
                rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin,
                                ymax=number_image_text_area.ymax)
                image_text_areas_min.append(rect_min)
                new_xmax = number_image_text_area.xmax + w // 2
                rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin,
                                ymax=number_image_text_area.ymax)
                image_text_areas_max.append(rect_max)
            image_text_areas.areas[Class_text.number] = image_text_areas_min
            res_labels_min = self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, image_text_areas)
            (number_text_min, _) = res_labels_min['number']
            if len(number_text_min) == self.danila_rama_text_recognize.get_number_length(rama_prod):
                return res_labels_min
            else:
                image_text_areas.areas[Class_text.number] = image_text_areas_max
                res_labels_max = self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, image_text_areas)
                (number_text_max, _) = res_labels_max['number']
                if len(number_text_max) == self.danila_rama_text_recognize.get_number_length(rama_prod):
                    return res_labels_max
                else:
                    return res_labels