from enum import Enum
class Class_detail(Enum):
    balka = 0
    rama = 1
    vagon = 2

class Class_detail_result:
    def __init__(self, class_detail, conf):
        self.class_detail = class_detail
        self.conf = conf