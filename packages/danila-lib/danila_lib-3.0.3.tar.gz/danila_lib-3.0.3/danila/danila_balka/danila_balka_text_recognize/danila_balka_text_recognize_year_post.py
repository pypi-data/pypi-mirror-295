class Danila_balka_text_recognize_year_post:
    def __init__(self, danila_balka_text_recognize):
        self.danila_balka_text_recognize = danila_balka_text_recognize

    def balka_text_recognize(self, balka_prod, img_cut, image_text_areas):
        res_labels = self.danila_balka_text_recognize.balka_text_recognize(balka_prod, img_cut, image_text_areas)
        (year_text, year_conf) = res_labels['year']
        if (len(year_text) == 2) and (int(year_text) < 25):
            res_labels['year'] = (year_text, year_conf)
        else:
            res_labels['year'] = ('24', 0.25)
        return res_labels
