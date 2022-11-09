import datetime

from query import (Query)


class Rasp:
    groups = [
        'БУ 1.20',
        'ВК 1.20',
        'ВК 1.21',
        'ВК 1.22',
        'ВК 1.9',
        'ДК 1.20',
        'ДК 1.21',
        'ДК 1.22',
        'ДК 2.21',
        'ИС 1.20',
        'ИС 1.21',
        'ИС 1.22',
        'ИС 1.9',
        'ИС 2.20',
        'ИС 2.21',
        'ИС 2.22',
        'КП 1.20',
        'КП 1.21',
        'КП 1.22',
        'КП 1.9',
        'КС 1.20',
        'МП 1.20',
        'МП 1.21',
        'МП 1.22',
        'МР 1.20',
        'МР 1.21',
        'МР 1.22',
        'МР 1.9',
        'НГ 1.22',
        'ПД 1.20',
        'ПД 1.21',
        'ПД 1.22',
        'ПД 1.9',
        'ПИ 1.20',
        'ПИ 1.21',
        'ПИ 1.22',
        'ПИ 1.9',
        'ПО 1.21',
        'ПО 1.22',
        'РЭ 1.20',
        'РЭ 1.21',
        'РЭ 1.22',
        'РЭ 1.9',
        'РЭ 2.20',
        'РЭ 2.21',
        'РЭ 2.22',
        'РЭ 2.9',
        'РЭ 3.20',
        'РЭ 3.21',
        'РЭ 3.22',
        'СВ 1.20',
        'СВ 1.21',
        'СВ 1.22',
        'ТК 1.20',
        'ТК 1.21',
        'ТК 1.22',
        'ТК 1.9',
        'ТМ 1.20',
        'ТМ 1.21',
        'ТМ 1.22',
        'ТМ 1.9'
    ]
    group: str
    date: str

    def __init__(self, text: str):
        self.text = text.split(' ')

    @staticmethod
    def validation_0(text: str):
        if text == '/rasp':
            return True
        return False

    def validation_1(self, text1: str, text2: str):
        for i in self.groups:
            if (text1 + " " + text2) == i:
                return True
        return False

    def validation_2(self, text: str):
        for i in ['сегодня', 'завтра', 'неделя']:
            if text == i:
                if i == 'сегодня':
                    self.date = datetime.datetime.now().strftime('%d.%m.%Y')
                elif i == 'завтра':
                    self.date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
                return True
        return False

    def valid(self):
        if self.validation_0(self.text[0]):
            if self.validation_1(self.text[1], self.text[2]):
                self.group = self.text[1] + " " + self.text[2]
                if self.validation_2(self.text[3]):
                    return True

    def query(self):
        return Query(url).week({
            "group_id": self.group,
            "date": self.date
        })

    def rasp(self):
        ras = ""
        rasp_t: dict = self.query()
        val = 0
        for i in rasp_t['data'][self.date]:
            if val != i['Пара']:
                ras += f"""
    - Пара:  <b>{i['Пара']}</b>
    - Наименование: 
    <b>{i['Наименование']}</b>
    - Преподаватель:  
    <b>{i['Преподаватель']}</b>
    - Блок:  <b>{i['Блок']}</b>
    - Кабинет:  <b>{i['Кабинет']}</b>
    - Время:  <b>{i['Время'][0]}-{i['Время'][1]}</b>
    --------------------------------------
    """
                val = i['Пара']
            else:
                continue
        return ras

url = "http://m.neftpk.ru/college/ws/Schedule.1cws"
