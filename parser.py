import os
import vk
import cv2
import json
import dlib
import urllib

import numpy as np

from tqdm import tqdm
from time import sleep
from pprint import pprint
from dotenv import load_dotenv
from multiprocessing import Pool

# METHOD #1: OpenCV, NumPy, and urllib

CHUNK_SIZE = 32
PROCESSES = 16

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

    dets, scores, idx = detector.run(image, 1, 0.5)

    face_features = []
    for i, d in enumerate(dets):
        shape = sp(image, d)

        face_descriptor = tuple(facerec.compute_face_descriptor(image, shape))

        face_features.append(face_descriptor)
    #     print("Detection {}, score: {}, face_type:{}".format(
    #         d, scores[i], idx[i]))

    #     cv2.rectangle(image, (d.left(), d.top()),
    #                   (d.right(), d.bottom()), (0, 0, 255), 2)

    # cv2.imshow("image", image)
    # cv2.waitKey()

    return face_features


def get_prepared_data(user_data):

    photos_data = user_data['photos_data']
    photo_albums = photos_data['items']

    prepared_data = {
        'id': user_data['id'],
        'domain': user_data['domain'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        "images": [],
    }

    for photo_album in photo_albums:
        photos = photo_album['sizes']

        photo = max(photos, key=lambda x: x['type'])

        image = url_to_image(photo['url'])
        try:
            face_features = get_face_features(image)
        except:
            continue

        if face_features:
            prepared_data['images'].append(
                {"image": photo['url'], "face_features": face_features})

    return prepared_data


def exists(id):

    for user_data in parsed_users_data:
        if user_data['id'] == id:
            return True
    return False


def users_data_generator(users_data, pbar, chunk_size=8):

    output = []
    for user_data in users_data:

        if user_data.get("is_closed") == False and not exists(user_data['id']):
            sleep(0.2)
            output.append({
                **user_data,
                "photos_data": vk_api.photos.getAll(owner_id=user_data['id'], v=version)
            })

        else:
            pbar.update()

        if len(output) == chunk_size:
            yield output
            output = []

    yield output


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

    first = vk_api.groups.getMembers(
        group_id=groupid, v=version)
    data = first["items"]
    count = first["count"] // 1000
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.

    with open("data_file.json", "w", encoding='utf8') as write_file, tqdm(total=first["count"]) as pbar, Pool(PROCESSES) as p:
        write_file.write('[')
        for i in range(1, count+1):
            users_ids = vk_api.groups.getMembers(
                group_id=groupid, v=version, offset=i*1000)["items"]

            users_raw_data = vk_api.users.get(
                user_ids=users_ids, v=version, fields=fields)

            #photos_data = vk_api.photos.getAll(owner_id=user_data['id'], v=version)

            # print(users_data)
            generator = users_data_generator(users_raw_data, pbar, chunk_size=CHUNK_SIZE)
            for users_data in generator:
                prepared_data = []
                try:
                    for user_data in p.imap_unordered(get_prepared_data, users_data):
                        pbar.update()

                        if user_data['images']:
                            prepared_data.append(user_data)

                    output_json = json.dumps(
                        prepared_data, indent=2, ensure_ascii=False)

                    output_json = output_json.strip("[]")
                    write_file.write(output_json)
                    write_file.write(',\n')
                except:
                    print("Error")

        write_file.seek(0, os.SEEK_END)
        write_file.seek(write_file.tell() - 3, os.SEEK_SET)
        write_file.write(']')


if __name__ == "__main__":

    with open('data_file copy.json', 'r', encoding='utf8') as parsed_data:
        parsed_users_data = json.load(parsed_data)

    print('avx -', dlib.USE_AVX_INSTRUCTIONS)
    print('blas -', dlib.DLIB_USE_BLAS)
    print('cuda -', dlib.DLIB_USE_CUDA)
    print('neon -', dlib.USE_NEON_INSTRUCTIONS)
    print('lapack -', dlib.DLIB_USE_LAPACK)

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    version = 5.126

    group_id = "leadersofdigital"

    token = os.environ.get("TOKEN")

    app_id = os.environ.get("APP_ID")
    login = os.environ.get("LOGIN")
    password = os.environ.get("PASSWORD")

    session = vk.AuthSession(app_id=app_id, user_login=login,
                             user_password=password, scope=4)  # access_token=token
    vk_api = vk.API(session)
    group_data = get_members(group_id)
