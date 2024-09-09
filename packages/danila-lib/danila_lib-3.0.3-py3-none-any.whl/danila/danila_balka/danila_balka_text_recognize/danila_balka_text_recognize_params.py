class Danila_balka_text_recognize_params:
    def __init__(self, balka_text_recognize_version):
        if balka_text_recognize_version < 40:
            year_post_num = balka_text_recognize_version // 20
            if year_post_num == 0:
                self.year_post = False
            else:
                self.year_post = True
            balka_text_recognize_version_20 = balka_text_recognize_version % 20
            prod_redone_num = balka_text_recognize_version_20 // 10
            self.prod_redone = (prod_redone_num == 1)
            balka_text_recognize_version_10 = balka_text_recognize_version_20 % 10
            self.balka_text_recognize_model_version = balka_text_recognize_version_10
            if balka_text_recognize_version_10 > 5:
                raise ValueError('rama_text_recognize_version - incorrect')
        else:
            raise ValueError('rama_text_recognize_version - incorrect')