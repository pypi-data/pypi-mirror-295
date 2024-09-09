from danila.danila_rama.danila_rama_classify import Danila_rama_classify
from danila.danila_rama.danila_rama_text_detect import Danila_rama_text_detect
from danila.danila_rama.danila_rama_text_recognize import Danila_rama_text_recognize
from data.neuro.prods import RAMA_PRODS
from data.result.Rama_prod import Rama_Prod
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_rama_redone:
    def __init__(self, local, yolov5_dir, danila_rama_params):
        self.danila_rama_params = danila_rama_params
        self.danila_rama_classify = Danila_rama_classify(local, yolov5_dir, self.danila_rama_params.danila_rama_classify_params)
        self.danila_rama_text_detect = Danila_rama_text_detect(local, yolov5_dir, self.danila_rama_params.danila_rama_text_detect_params)
        self.danila_rama_text_recognize = Danila_rama_text_recognize(local, yolov5_dir, self.danila_rama_params.danila_rama_text_recognize_params)

    def rama_classify(self,img, detail):
        rama_prod_conf = self.danila_rama_classify.rama_classify(img)
        if detail is None:
            detail_prod = Text_cut_recognize_result('rama', 1)
            det = Text_recognize_result(detail_prod)
        else:
            det = detail
        if rama_prod_conf.rama_prod != Rama_Prod.no_rama:
            text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
            det.prod = Text_cut_recognize_result(text_prod, rama_prod_conf.conf)
        return det

    def rama_text_detect(self, img):
        rama_prod_conf = self.danila_rama_classify.rama_classify(img)
        result_img = img
        if rama_prod_conf.rama_prod != Rama_Prod.no_rama:
            result_img = self.danila_rama_text_detect.rama_text_detect(img, rama_prod_conf.rama_prod)
        return result_img

    def rama_text_recognize(self, img, detail):
        rama_prod_conf = self.danila_rama_classify.rama_classify(img)
        if detail is None:
            detail_prod = Text_cut_recognize_result('rama', 1)
            det = Text_recognize_result(detail_prod)
        else:
            det = detail
        if rama_prod_conf.rama_prod != Rama_Prod.no_rama:
            text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
            det.prod = Text_cut_recognize_result(text_prod, rama_prod_conf.conf)
            img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img, rama_prod_conf.rama_prod)

            res_labels = self.danila_rama_text_recognize.rama_text_recognize(rama_prod_conf.rama_prod, img_cut, img_text_areas)
            res_labels_prod_text, res_labels_prod_conf = res_labels['prod']
            if res_labels_prod_text != text_prod:
                if res_labels_prod_text == '1923':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.altai)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.altai, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '1487':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.balakovo)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.balakovo, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '12':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(text_prod, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.begickaya)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.begickaya, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '33':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.promlit)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.promlit, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '1275':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.ruzhimmash)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.ruzhimmash, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '1378':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.tihvin)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.tihvin, img_cut,
                                                                                     img_text_areas)
                elif res_labels_prod_text == '5':
                    text_prod = RAMA_PRODS[rama_prod_conf.rama_prod]
                    det.prod = Text_cut_recognize_result(res_labels_prod_text, rama_prod_conf.conf)
                    img_cut, img_text_areas = self.danila_rama_text_detect.rama_rext_detect_cuts(img,
                                                                                                 Rama_Prod.uralvagon)
                    res_labels = self.danila_rama_text_recognize.rama_text_recognize(Rama_Prod.uralvagon, img_cut,
                                                                                     img_text_areas)
            res_labels_number_text, res_labels_number_conf = res_labels['number']
            det.number = Text_cut_recognize_result(res_labels_number_text, res_labels_number_conf)
            res_labels_year_text, res_labels_year_conf = res_labels['year']
            det.year = Text_cut_recognize_result(res_labels_year_text, res_labels_year_conf)
        return det