import requests
from bs4 import BeautifulSoup


def inn_parser(fio):
    url = 'https://kontragent.skrin.ru/SearchIchp/IchpDoSearch'

    data = {
        "ruler": "Лом-Али Якубов",
        "reg_type": 1,
        "reg_excl": 0,
        "ind_main": 0,
        "ind_excl": 0,
        "page_no": 1,
        "rcount": 30,
        "user_id": 0,
        "group_id": 0,
        "is_covid": 0,
        "covidOked": 0,
        "status": 0,
        "top1000": 0,
    }

    task = requests.post(url, data=data)
    s = BeautifulSoup(task.text, 'html.parser')

    inn = s.find('span', 'code_title_ip', text='ИНН:').parent.contents[1]

    return inn

if __name__ == "__main__":
    inn_parser("Лом-Али Якубов")