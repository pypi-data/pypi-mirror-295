from data.result.Class_text import Class_text




class Danila_rama_text_recognize_work:
    def __init__(self, text_recognize_model, prod_coefficients):
        self.text_recognize_model = text_recognize_model
        self.prod_coefficients = prod_coefficients

    def rama_text_recognize(self, img_cut, image_text_areas):
        label_area = self.text_recognize_model.work_image_cut(
            image_text_areas, img_cut,
            self.prod_coefficients.number_coefficients.length,
            self.prod_coefficients.number_coefficients.height,
            self.prod_coefficients.number_coefficients.width,
            self.prod_coefficients.prod_coefficients.length,
            self.prod_coefficients.prod_coefficients.height,
            self.prod_coefficients.prod_coefficients.width,
            self.prod_coefficients.year_coefficients.length,
            self.prod_coefficients.year_coefficients.height,
            self.prod_coefficients.year_coefficients.width
        )
        res_labels = {}
        (number_text, number_conf) = label_area.labels[Class_text.number]
        res_labels['number'] = (number_text, number_conf)
        (year_text, year_conf) = label_area.labels[Class_text.year]
        res_labels['year'] = (year_text, year_conf)
        (prod_text, prod_conf) = label_area.labels[Class_text.prod]
        res_labels['prod'] = (prod_text, prod_conf)
        return res_labels
