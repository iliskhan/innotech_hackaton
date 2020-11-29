from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

import os
import vk
import cv2
import json
import dlib
import urllib

import numpy as np
import ssl

from dotenv import load_dotenv
from scipy.spatial import distance
from django.conf import settings


from .models import VkUserPersonal, VkUserData, VkUserEducation, VkUserOccupation, OccupationType
from .serializers import VkUserOccupationSerializer, VkUserPersonalSerializer, VkUserEducationSerializer, VkUserDataSerializer, VkUserDataDetailSerializer


def write_json(data, filename='data.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)


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

        dotenv_path = os.path.join(settings.BASE_DIR, '.env')

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        token = os.environ.get("TOKEN")

        self.app_id = os.environ.get("APP_ID")
        self.login = os.environ.get("LOGIN")
        self.password = os.environ.get("PASSWORD")


        ssl._create_default_https_context = ssl._create_unverified_context
        session = vk.Session(access_token=token)

        self.vk_api = vk.API(session)

        predictor_path = "/app/main/shape_predictor_5_face_landmarks.dat"
        face_rec_model_path = "/app/main/dlib_face_recognition_resnet_model_v1.dat"

        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(predictor_path)
        self.facerec = dlib.face_recognition_model_v1(face_rec_model_path)

        self.face_features_path = '/app/main/face_features.json'

    def get_face_features(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        dets, scores, idx = self.detector.run(image, 1, 0.5)

        face_features = []
        for i, d in enumerate(dets):
            shape = self.sp(image, d)

            face_descriptor = tuple(self.facerec.compute_face_descriptor(image, shape))

            face_features.append(face_descriptor)

        return face_features

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

        with open(self.face_features_path, encoding='utf8') as ff:
            data = json.load(ff)

            temp = data['face_features']

            ids = [list(element.keys())[0] for element in temp]

            if not str(user_data['id']) in ids:
                temp.append({user_data['id']: face_features})

        write_json(data, filename=self.face_features_path)

        return user_data

    def recognition(self, image):

        image = np.asarray(bytearray(image), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # image = cv2.imread(image)
        #
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        dets, scores, idx = self.detector.run(image, 1, 0.5)

        incoming_face_feature = None

        for i, d in enumerate(dets):
            shape = self.sp(image, d)

            incoming_face_feature = np.array(
                self.facerec.compute_face_descriptor(image, shape), dtype=np.float64)



        with open(self.face_features_path, "r", encoding="utf8") as ff:
            face_features = json.load(ff)

        ids_with_errors = []

        face_features = face_features['face_features']

        for item in face_features:
            for face_feature in item.values():
                if len(face_feature) == 0:
                    break

                face_feature = np.array(face_feature)

                ids_with_errors.append(
                    {"id": item.keys(), "error": distance.euclidean(face_feature, incoming_face_feature)})

        min_error = min(ids_with_errors, key=lambda x: x['error'])
        if min_error['error'] > 0.6:
            return None
        return list(min_error["id"])[0]


vk_parser = VkParser()


class VkApiView(APIView):


    @transaction.atomic
    def post(self, request):
        vk_link = request.data.get('link')
        vk_user_data = vk_parser.get_user_data_by_url(vk_link)
        education, personal, occupation = None, None, None
        if vk_user_data.get('occupation'):
            occupation = vk_user_data.get('occupation')
            occupation_type = getattr(OccupationType, occupation.get('type'))
            occupation['type'] = occupation_type
            ser = VkUserOccupationSerializer(data=vk_user_data.get('occupation'))
            ser.is_valid(raise_exception=True)
            ser.save()
            occupation = ser.data['id']
        if vk_user_data.get('personal'):
            personal = vk_user_data.get('personal')
            langs = personal.get('langs')
            if langs:
                langs = ','.join(langs)
            personal['langs'] = langs
            ser = VkUserPersonalSerializer(data=personal)
            ser.is_valid(raise_exception=True)
            ser.save()
            personal = ser.data['id']

        if vk_user_data.get('universities'):
            education = vk_user_data.get('universities')[0]
            education_data = {
                'university': education.get('name'),
                'faculty': education.get('faculty_name'),
                'graduation': education.get('graduation')
            }
            ser = VkUserEducationSerializer(data=education_data)
            ser.is_valid(raise_exception=True)
            ser.save()
            education = ser.data['id']

        if occupation:
            vk_user_data['occupation'] = occupation
        if education:
            vk_user_data['education'] = education
        if personal:
            vk_user_data['personal'] = personal


        vk_user_data['vk_user_id'] = vk_user_data['id']
        if  vk_user_data.get('country'):
            vk_user_data['country'] = vk_user_data['country']['title']

        if vk_user_data.get('bdate'):
            vk_user_data['bdate'] = '-'.join(list(reversed(vk_user_data['bdate'].split('.'))))
            if len(vk_user_data['bdate']) < 8:
                vk_user_data['bdate'] = None
        vk_user_data['avatar'] = vk_user_data['photo_max_orig']
        serializer = VkUserDataSerializer(data=vk_user_data)
        if vk_user_data.get('city'):
            vk_user_data['city'] = vk_user_data['city']['title']
        serializer.is_valid(raise_exception=True)
        serializer.save()

        vk_user = VkUserData.objects.get(pk=serializer.data['id'])
        response_serializer = VkUserDataDetailSerializer(vk_user)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, vk_user_id):
        vk_user = VkUserData.objects.filter(vk_user_id=vk_user_id).first()
        serializer = VkUserDataDetailSerializer(vk_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VkImageApiView(APIView):
    def post(self, request):
        image = request.data['image'].read()
        vk_user_id = vk_parser.recognition(image)
        if not vk_user_id:
            return Response('Пользователь не найден', status=status.HTTP_404_NOT_FOUND)
        vk_user = VkUserData.objects.filter(vk_user_id=vk_user_id).first()
        serializer = VkUserDataDetailSerializer(vk_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
