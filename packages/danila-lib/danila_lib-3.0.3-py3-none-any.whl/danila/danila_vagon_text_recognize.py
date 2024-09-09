from danila.danila_vagon.danila_vagon_text_recognize_base import Danila_vagon_text_recognize_base


class Danila_vagon_text_recognize:
    def __init__(self, local, yolov5_dir, danila_vagon_text_recognize_params):
        self.danila_vagon_text_recognize = Danila_vagon_text_recognize_base(local, yolov5_dir, danila_vagon_text_recognize_params)

    def vagon_number_recognize(self, img, vagon_number_rects):
        return self.danila_vagon_text_recognize.vagon_number_recognize(img, vagon_number_rects)