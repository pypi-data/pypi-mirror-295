from danila.danila_vagon.danila_vagon_text_detect_base import Danila_vagon_text_detect_base


class Danila_vagon_text_detect:
    def __init__(self, local, yolov5_dir, vagon_text_detect_params):
        self.danila_vagon_text_detect = Danila_vagon_text_detect_base(local, yolov5_dir, vagon_text_detect_params)

    def vagon_number_detect(self, img):
        return self.danila_vagon_text_detect.vagon_number_detect(img)

    def vagon_number_detect_rects(self, img):
        return self.danila_vagon_text_detect.vagon_number_detect_rects(img)