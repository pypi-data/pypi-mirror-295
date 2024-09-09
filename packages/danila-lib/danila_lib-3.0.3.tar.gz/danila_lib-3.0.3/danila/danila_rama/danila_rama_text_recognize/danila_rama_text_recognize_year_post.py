class Danila_rama_text_recognize_year_post:
    def __init__(self, danila_rama_text_recognize):
        self.danila_rama_text_recognize = danila_rama_text_recognize

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        res_labels = self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, image_text_areas)
        (year_text, year_conf) = res_labels['year']
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('23', 0.25)
        return res_labels

    def get_number_length(self, rama_prod):
        return self.danila_rama_text_recognize.get_number_length(rama_prod)