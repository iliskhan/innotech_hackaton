import vk
import cv2
import json
import dlib
import urllib

import numpy as np

from tqdm import tqdm
from pprint import pprint
from multiprocessing import Pool

# METHOD #1: OpenCV, NumPy, and urllib

predictor_path = "./shape_predictor_5_face_landmarks.dat"
face_rec_model_path = "./dlib_face_recognition_resnet_model_v1.dat"

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


def get_face_features(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    dets, scores, idx = detector.run(image, 1, 0)

    face_features = []
    for i, d in enumerate(dets):
        shape = sp(image, d)

        face_descriptor = list(facerec.compute_face_descriptor(image, shape))

        face_features.append(face_descriptor)
    #     print("Detection {}, score: {}, face_type:{}".format(
    #         d, scores[i], idx[i]))

    #     cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), (0,0,255), 2)

    # cv2.imshow("image", image)
    # cv2.waitKey()

    return face_features

def get_prepared_data(user_data):
    image_url = user_data['photo_max_orig']

    if image_url != "https://vk.com/images/camera_400.png":
        image = url_to_image(image_url)

        face_features = get_face_features(image)

        if face_features:
            user_data.update({"face_features": face_features})

            return user_data




def get_members(groupid, version=5.126):

    fields = [
        # 'tv',
        # 'sex',
        # 'city',
        # 'music',
        # 'bdata',
        # 'books',
        # 'games',
        # 'quotes',
        # 'movies',
        # 'career',
        'domain',
        # 'country',
        # 'schools',
        # 'timezone',
        # 'relation',
        # 'personal',
        # 'nickname',
        # 'military',
        # 'contacts',
        # 'verified',
        # 'relatives',
        # 'home_town',
        # 'interests',
        # 'education',
        # 'last_seen',
        # 'occupation',
        # 'connections',
        # 'universities',
        'photo_max_orig',
        # 'followers_count',
    ]

    first = vk_api.groups.getMembers(group_id=groupid, v=version)  # Первое выполнение метода
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    # Присваиваем переменной количество тысяч участников
    count = first["count"] // 1000
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    with open("data_file.json", "w") as write_file, tqdm(total= first["count"]) as pbar, Pool() as p:
    
        for i in range(1, count+1):
            users_ids = vk_api.groups.getMembers(group_id=groupid, v=version, offset=i*1000)["items"]

            users_data = vk_api.users.get(user_ids=users_ids, v=version, fields=fields)
            prepared_data = []
            
            for user_data in map(get_prepared_data, users_data):
                pbar.update()

                if user_data:
                    prepared_data.append(user_data)
            
            print("Обработано аккаунтов =", len(prepared_data))
            json.dump(prepared_data, write_file, indent=2, ensure_ascii=False)



if __name__ == "__main__":

    print('blas -'  , dlib.DLIB_USE_BLAS)
    print('cuda -'  , dlib.DLIB_USE_CUDA)
    print('lapack -', dlib.DLIB_USE_LAPACK)
    print('avx -'   , dlib.USE_AVX_INSTRUCTIONS)
    print('neon -'  , dlib.USE_NEON_INSTRUCTIONS)
    version = 5.126

    token = "67d5f87b67d5f87b67d5f87b8967a0d9ae667d567d5f87b386bf39149edfb44b47ab50d"

    group_id = "leadersofdigital"

    session = vk.Session(access_token=token)
    vk_api = vk.API(session)
    group_data = get_members(group_id)
