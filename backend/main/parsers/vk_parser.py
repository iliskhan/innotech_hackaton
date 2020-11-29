import os
import vk
import cv2
import json
import dlib
import urllib

import numpy as np
import ssl

from pprint import pprint
from dotenv import load_dotenv
from scipy.spatial import distance
from pathlib import Path


class VkParser:
    def __init__(self):

        self.map_distance_compute = np.vectorize(distance.euclidean, signature='(n),(m)->()')

        self.fields = [
            'sex',
            'city',
            'bdate',
            'career',
            'country',
            'schools',
            'relation',
            'personal',
            'nickname',
            'contacts',
            'interests',
            'education',
            'occupation',
            'universities',
            'photo_max_orig',
        ]

        self.version = 5.126

        dotenv_path = os.path.join(Path(__file__).resolve().parent.parent.parent, '.env')

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        token = os.environ.get("TOKEN")
        print(dotenv_path)

        app_id = os.environ.get("APP_ID")
        login = os.environ.get("LOGIN")
        password = os.environ.get("PASSWORD")

        ssl._create_default_https_context = ssl._create_unverified_context

        session = vk.AuthSession(app_id=app_id, user_login=login,
                                 user_password=password, scope=4)

        self.vk_api = vk.API(session)

        predictor_path = "./shape_predictor_5_face_landmarks.dat"
        face_rec_model_path = "./dlib_face_recognition_resnet_model_v1.dat"

        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(predictor_path)
        self.facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    def get_face_features(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        dets, scores, idx = self.detector.run(image, 1, 0.5)

        face_features = []
        for i, d in enumerate(dets):
            shape = self.sp(image, d)

            face_descriptor = np.array(self.facerec.compute_face_descriptor(image, shape), dtype=np.float64)

            face_features.append(face_descriptor)

        return np.array(face_features)

    def url_to_image(self, image_url):

        resp = urllib.request.urlopen(image_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    def get_user_data_by_url(self, url):

        user_id = url.split('/')[-1]

        user_data = self.vk_api.users.get(user_ids=[user_id], v=self.version, fields=self.fields)[0]

        image = self.url_to_image(user_data['photo_max_orig'])

        face_features = self.get_face_features(image)

        user_data.update({'face_features': face_features})

        return user_data


if __name__ == "__main__":
    vk_parser = VkParser()

    pprint(vk_parser.get_user_data_by_url("https://vk.com/iliskhan_gudaev"))
    # pprint(vk_parser.get_user_data_by_url("https://vk.com/lomali93"))