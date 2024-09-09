from danila.danila_balka.danila_balka_classify.Danila_balka_classify import Danila_balka_classify
from danila.danila_balka.danila_balka_text_detect.danila_balka_text_detect import Danila_balka_text_detect
from danila.danila_balka.danila_balka_text_recognize.danila_balka_text_recognize import Danila_balka_text_recognize
from data.neuro.prods import BALKA_PRODS
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result
from data.result.balka_prod import Balka_Prod


class Danila_balka_redone:
    def __init__(self, yolov5_dir, danila_balka_params):
        self.danila_balka_params = danila_balka_params
        self.danila_balka_classify = Danila_balka_classify(yolov5_dir, self.danila_balka_params.danila_balka_classify_params)
        self.danila_balka_text_detect = Danila_balka_text_detect(yolov5_dir,
                                                               self.danila_balka_params.danila_balka_text_detect_params)
        self.danila_balka_text_recognize = Danila_balka_text_recognize(yolov5_dir, self.danila_balka_params.danila_balka_text_recognize_params)


    def balka_classify(self,img, detail):
        balka_prod_conf = self.danila_balka_classify.balka_classify(img)
        if detail is None:
            detail_prod = Text_cut_recognize_result('balka', 1)
            det = Text_recognize_result(detail_prod)
        else:
            det = detail
        if balka_prod_conf.balka_prod != Balka_Prod.no_balka:
            text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
            det.prod = Text_cut_recognize_result(text_prod, balka_prod_conf.conf)
        return det

    def balka_text_detect(self, img):
        balka_prod_conf = self.danila_balka_classify.balka_classify(img)
        result_img = img
        if balka_prod_conf.balka_prod != Balka_Prod.no_balka:
            result_img = self.danila_balka_text_detect.balka_text_detect(img, balka_prod_conf.balka_prod)
        return result_img

    def balka_text_recognize(self, img, detail):
        balka_prod_conf = self.danila_balka_classify.balka_classify(img)
        if detail is None:
            detail_prod = Text_cut_recognize_result('balka', 1)
            det = Text_recognize_result(detail_prod)
        else:
            det = detail
        if balka_prod_conf.balka_prod != Balka_Prod.no_balka:
            text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
            det.prod = Text_cut_recognize_result(text_prod, balka_prod_conf.conf)
            img_cuts, img_text_areas_2_balkas = self.danila_balka_text_detect.balka_rext_detect_cuts(img, balka_prod_conf.balka_prod)

            res_labels = self.danila_balka_text_recognize.balka_text_recognize(
                balka_prod=balka_prod_conf.balka_prod,
                img_cuts=img_cuts,
                img_text_areas_2_balkas=img_text_areas_2_balkas)
            res_labels_prod_text, res_labels_prod_conf = res_labels['prod']
            if res_labels_prod_text != text_prod:
                if res_labels_prod_text == '1923':
                    text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, balka_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_balka_text_detect.balka_rext_detect_cuts(img,
                                                                                                 Balka_Prod.altai)
                    res_labels = self.danila_balka_text_recognize.balka_text_recognize(Balka_Prod.altai, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '12':
                    text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, balka_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_balka_text_detect.balka_rext_detect_cuts(img,
                                                                                                 Balka_Prod.begickaya)
                    res_labels = self.danila_balka_text_recognize.balka_text_recognize(Balka_Prod.begickaya, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '33':
                    text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, balka_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_balka_text_detect.balka_rext_detect_cuts(img,
                                                                                                   Balka_Prod.promlit)
                    res_labels = self.danila_balka_text_recognize.balka_text_recognize(Balka_Prod.promlit, img_cut,
                                                                                       img_text_areas)
                elif res_labels_prod_text == '1275':
                    text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, balka_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_balka_text_detect.balka_rext_detect_cuts(img,
                                                                                                   Balka_Prod.ruzhimmash)
                    res_labels = self.danila_balka_text_recognize.balka_text_recognize(Balka_Prod.ruzhimmash, img_cut,
                                                                                       img_text_areas)
                elif res_labels_prod_text == '1378':
                    text_prod = BALKA_PRODS[balka_prod_conf.balka_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, balka_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_balka_text_detect.balka_rext_detect_cuts(img,
                                                                                                   Balka_Prod.tihvin)
                    res_labels = self.danila_balka_text_recognize.balka_text_recognize(Balka_Prod.tihvin, img_cut,
                                                                                       img_text_areas)
            res_labels_number_text, res_labels_number_conf = res_labels['number']
            det.number = Text_cut_recognize_result(res_labels_number_text, res_labels_number_conf)
            res_labels_year_text, res_labels_year_conf = res_labels['year']
            det.year = Text_cut_recognize_result(res_labels_year_text, res_labels_year_conf)
        return det