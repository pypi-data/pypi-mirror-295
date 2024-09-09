class Danila_rama_text_recognize_prod_redone:

    def __init__(self, danila_rama_text_recognize):
        self.danila_rama_text_recognize = danila_rama_text_recognize

    def rama_text_recognize(self, rama_prod, img_cut, image_text_areas):
        return self.danila_rama_text_recognize.rama_text_recognize(rama_prod, img_cut, image_text_areas)

    def get_number_length(self, rama_prod):
        return self.danila_rama_text_recognize.get_number_length(rama_prod)