import hashlib
import json
import os
from datetime import datetime

import cv2
import torch
from tensorflow import keras
import numpy as np

from data.neuro.models import *
from data.result.Class_im import *
import zipfile
import requests
from urllib.parse import urlencode

class Detail_classify_yolo_dop_yolo_dop_CNN:
    def __init__(self, local, yolo_dir, detail_classify_CNN, detail_classify_yolo, balka_detect, rama_detect, vagon_detect):
        if local:
            self.detail_classify_CNN_model = keras.models.load_model(detail_classify_CNN)
            self.detail_classify_yolo_model = torch.hub.load(yolo_dir, 'custom', detail_classify_yolo, source='local')
            self.rama_detect_model = torch.hub.load(yolo_dir, 'custom', rama_detect, source='local')
            self.balka_detect_model = torch.hub.load(yolo_dir, 'custom', balka_detect, source='local')
            self.vagon_number_detect_model = torch.hub.load(yolo_dir, 'custom', vagon_detect, source='local')
        else:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

            public_key = detail_classify_CNN  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']

            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            # print(download_response.content)

            # print(download_response.content)
            with open('detail_classify_model.zip', 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile('detail_classify_model.zip', 'r') as zip_ref:
                zip_ref.extractall()
            self.detail_classify_CNN_model = keras.models.load_model('detail_classify_model.h5')

            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = detail_classify_yolo  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'detail_classify.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'detail_classify.pt'
            self.detail_classify_yolo_model = torch.hub.load(yolo_dir, 'custom', weights_file_path, source='local')

            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = rama_detect  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'rama_detect.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'rama_detect.pt'
            self.rama_detect_model = torch.hub.load(yolo_dir, 'custom', weights_file_path, source='local')

            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = balka_detect  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'balka_detect.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'balka_detect.pt'
            self.balka_detect_model = torch.hub.load(yolo_dir, 'custom', weights_file_path, source='local')

            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = vagon_detect  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            zip_path = 'vagon_number_detect.zip'
            # print(download_response.content)
            with open(zip_path, 'wb') as f:
                f.write(download_response.content)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall()
            weights_file_path = 'vagon_number_detect.pt'
            self.vagon_number_detect_model = torch.hub.load(yolo_dir, 'custom', weights_file_path, source='local')






    def classify(self, image_initial):
        """classify(img:openCV frame):Class_im - classify openCV img with CNN, returns Class_im"""
        hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        hash_str = hash_object.hexdigest()
        initial_image_path = 'initial_image' + hash_str + '.jpg'
        cv2.imwrite(initial_image_path, image_initial)

        img = cv2.imread(initial_image_path)
        results = self.detail_classify_yolo_model([initial_image_path], size=512)
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        if len(res2) == 0:
            conf = [0.0, 0.0, 0.0]
            results_balka = self.balka_detect_model([initial_image_path])
            json_res_balka = results_balka.pandas().xyxy[0].to_json(orient="records")
            res2_balka = json.loads(json_res_balka)
            if len(res2_balka) > 0:
                conf[0] = res2_balka[0]['confidence']
            results_rama = self.rama_detect_model([initial_image_path])
            json_res_rama = results_rama.pandas().xyxy[0].to_json(orient="records")
            res2_rama = json.loads(json_res_rama)
            if len(res2_rama) > 0:
                conf[1] = res2_rama[0]['confidence']
            results_vagon = self.vagon_number_detect_model([initial_image_path])
            json_res_vagon = results_vagon.pandas().xyxy[0].to_json(orient="records")
            res2_vagon = json.loads(json_res_vagon)
            if len(res2_vagon) > 0:
                conf[2] = res2_vagon[0]['confidence']
            if (conf[0] == 0.0) & (conf[1] == 0.0) & (conf[2] == 0.0):
                img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_grey_size = cv2.resize(img_grey, (512, 512))
                data = np.array(img_grey_size, dtype="float") / 255.0
                data = data.reshape((1, 512, 512))
                res = self.detail_classify_CNN_model.predict(data)
                res_list = res[0].tolist()
                res_index = res_list.index(max(res_list))
                conf_res = res_list[res_index]
            else:
                res_index = conf.index(max(conf))
                conf_res = max(conf)
        else:
            res_index = res2[0]['class']
            conf_res = res2[0]['confidence']
        class_detail = Class_detail(res_index)
        os.remove(initial_image_path)
        return Class_detail_result(class_detail, round(conf_res, 2))
