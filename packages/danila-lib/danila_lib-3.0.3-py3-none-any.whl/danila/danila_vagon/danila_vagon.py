from danila.danila_vagon.danila_vagon_text_detect import Danila_vagon_text_detect
from danila.danila_vagon.danila_vagon_text_recognize import Danila_vagon_text_recognize
from data.result.Text_cut_recognize_result import Text_cut_recognize_result
from data.result.Text_recognize_result import Text_recognize_result


class Danila_vagon:
    def __init__(self, local, yolov5_dir, danila_vagon_params):
        self.danila_vagon_params = danila_vagon_params
        self.danila_vagon_text_detect = Danila_vagon_text_detect(local, yolov5_dir, self.danila_vagon_params.danila_vagon_text_detect_params)
        self.danila_vagon_text_recognize = Danila_vagon_text_recognize(local, yolov5_dir, self.danila_vagon_params.danila_vagon_text_recognize_params)

    def vagon_number_detect(self, img):
        self.danila_vagon_text_detect.vagon_number_detect(img)

    def vagon_number_recognize(self, img, detail = None):
        det = detail
        vagon_number_rects = self.danila_vagon_text_detect.vagon_number_detect_rects(img)
        if det is None:
            det = Text_recognize_result(Text_cut_recognize_result('vagon', 1.0))
        if len(vagon_number_rects) == 0:
            return det
        detail_number_text, detail_number_conf =  self.danila_vagon_text_recognize.vagon_number_recognize(img, vagon_number_rects)
        det.number = Text_cut_recognize_result(detail_number_text, round(detail_number_conf, 2))
        return det