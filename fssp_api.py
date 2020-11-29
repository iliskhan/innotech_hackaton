import requests
from time import sleep

base_url = "https://api-ip.fssp.gov.ru/api/v1.0/"


"""
    return something(json) like this:
    {
        'status': 'success',
        'code': 0,
        'exception': '',
        'response': {
            'status': 0,
            'task_start': '2020-11-28 20:16:44',
            'task_end': '2020-11-28 20:16:45',
            'result': [
                {
                    'status': 0,
                    'query': {
                        'type': 1,
                        'params': {
                            'region': '-1',
                            'firstname': 'варламов',
                            'secondname': None,
                            'lastname': 'илья',
                            'birthdate': None
                        }
                    },
                    'result': []
                }
            ]
        }
    }
with data in result ================================================================================
    {
        'status': 'success',
        'code': 0,
        'exception': '',
        'response': {
            'status': 0,
            'task_start': '2020-11-28 20:16:44',
            'task_end': '2020-11-28 20:16:45',
            'result': [
                {
                    'status': 0,
                    'query': {
                        'type': 1,
                        'params': {
                            'region': '-1',
                            'firstname': 'варламов',
                            'secondname': None,
                            'lastname': 'илья',
                            'birthdate': None
                        }
                    },
                    'result': [
                        {
                            'name': 'ВАРЛАМОВ ИЛЬЯ МИХАЙЛОВИЧ 07.01.1985 ГОР. МОСКВА',
                            'exe_production': '40770/17/77010-ИП от 07.02.2017',
                            'details': 'Судебный приказ от 22.04.2016 № 2-383/2016 СУДЕБНЫЙ УЧАСТОК №\xa096 ОСТАНКИНСКОГО СУДЕБНОГО РАЙОНА Г. МОСКВЫ',
                            'subject': 'Задолженность по кредитным платежам (кроме ипотеки)',
                            'department': 'Останкинский ОСП 129347, г. Москва, Югорский проезд, д. 22. стр. 1',
                            'bailiff': 'БАДИКОВА Ю. И. +7(499)558-16-04<br>+7(499)558-16-04<br>',
                            'ip_end': '2018-02-12, 46, 1, 3'
                        },
                    ]
                }
            ]
        }
    }
"""

def get_from_fssp_info(
    firstname,
    secondname,
    lastname,
    region,
    birthdate,
):

    data = {
        "token": "J9PeHtr5m1xw",
        "region": region,
        "firstname": firstname,
        "secondname": secondname,
        "lastname": lastname,
        "birthdate": birthdate,                                        #07.01.1984
    }

    task_response = requests.get(base_url + "search/physical", params=data)
    task = task_response.json().get('response')['task']

    data_task = {
        "token": "J9PeHtr5m1xw",
        "task": task,
    }

    result = requests.get(base_url + "result", params=data_task).json()
    while result.get('response')['status'] != 0:
        result = requests.get(base_url + "result", params=data_task).json()
        sleep(2)

    return result