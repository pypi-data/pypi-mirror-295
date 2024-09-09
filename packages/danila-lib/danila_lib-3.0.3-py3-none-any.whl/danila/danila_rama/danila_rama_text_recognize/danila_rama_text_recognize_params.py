class Danila_rama_text_recognize_params:
    def __init__(self, rama_text_recognize_version):
        if (rama_text_recognize_version < 80):
            year_post_num = rama_text_recognize_version // 40
            if year_post_num == 0:
                self.year_post = False
            else:
                self.year_post = True
            rama_text_recognize_version_40 = rama_text_recognize_version % 40
            number_shift_num = rama_text_recognize_version_40 // 20
            self.number_shift = (number_shift_num == 1)
            rama_text_recognize_version_20 = rama_text_recognize_version_40 % 20
            prod_redone_num = rama_text_recognize_version_20 // 10
            self.prod_redone = (prod_redone_num == 1)
            rama_text_recognize_version_10 = rama_text_recognize_version_20 % 10
            self.rama_text_recognize_model_version = rama_text_recognize_version_10
            if rama_text_recognize_version_10 > 6:
                raise ValueError('rama_text_recognize_version - incorrect')
        else:
            raise ValueError('rama_text_recognize_version - incorrect')




