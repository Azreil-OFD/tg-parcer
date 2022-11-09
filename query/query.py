class Query:
    """
    Класс для взаимодействия с API колледжа
    """

    try:
        import requests
        import xmltodict
        import re as regex
        import datetime
    except:
        print("= -= установи парочку нужных мне модулей: requests , xmltodict")

    regular_data: str = '^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\\2))(?:(?:1[6-9]|[2-9]\d)?\d\{2\})$|^(?:29(\/|-|\.)0?2\\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'
    group_id = ""
    date = ""
    server_url: str

    def __init__(self, api_url: str) -> None:
        """
        Инициализация:
            Входные пеараметры:
                api_url : str - url api колледжа , для подключения
                желательно хранить в .env
        """
        self.server_url = api_url

    class conveyor:
        """
        Класс для форматирования входных данных
        """

        def __init__(self, data: dict) -> list:
            data = self.rename(data)
            self.data = self.sort_and_configure(data)

        @staticmethod
        def rename(data: dict) -> list:
            """
            Переименование значений
            """
            rename = {
                'm:UF_ID_TEACHER': "Преподаватель",
                'm:UF_PARA': 'UF_PARA',
                'm:UF_ZONE': 'Блок',
                'm:UF_LECTURE': 'Кабинет',
                'm:UF_DATE': 'Дата',
                'm:UF_ID_SUBJECT':'Наименование'
            }
            reneme_para_result = {}
            reneme_result = []

            data = data

            for i in data:
                for j in rename:
                    
                    if (j == 'm:UF_ID_SUBJECT'):
                        s : str = str(i[j])
                        s_bec = s
                        ss = s.split(' ')
                        if (s[0] == 'М'):
                            if (s[1] == 'Д'):
                                if (s[2] == 'К'):
                                    s = ss[0]
                        elif(len(s) > 16):
                            if(len(ss)) > 2:
                                s = f"{ss[0]} {ss[1]}"
                                if (ss[1] + ' ' + ss[2]) == "Учебная практика":
                                    s = s_bec
                        reneme_para_result[rename[j]] = s
                        continue
                    if (j == 'm:UF_LECTURE'):
                        s : str = str(i[j])
                        cabin : str = ""
                        for cab in s:
                            if cab == ' ':
                                break
                            if cab == '_':
                                break
                            cabin += cab
                        reneme_para_result[rename[j]] = cabin
                        continue
                    if (j == 'm:UF_ZONE'):
                        s : str = str(i[j])
                        if (s == 'Учебно-производственный корпус'):
                            s = "П"
                        elif (s == 'Учебно-административный корпус'):
                            s = ""
                        elif (s == 'Физкультурный корпус'):
                            s = "С"
                        reneme_para_result[rename[j]] = s
                        continue
                    if (j == 'm:UF_ID_TEACHER'):
                        s : str = str(i[j])
                        if s == "Вакансия":
                            reneme_para_result[rename[j]] = str(i[j])
                            continue
                        s_l = s.split(' ')
                        reneme_para_result[rename[j]] = f'{s_l[0]} {s_l[1][0:1]}.{s_l[2][0:1]}.'
                        continue  
                    reneme_para_result[rename[j]] = str(i[j])

                reneme_result.append(reneme_para_result)
                reneme_para_result = {}

            return reneme_result

        @staticmethod
        def sort_and_configure(data: list) -> dict:
            """
            Метод для сортировки пар по датам
            """

            para = {
                1: 1,
                2: 1,
                3: 2,
                4: 2,
                5: 3,
                6: 3,
                7: 4,
                8: 4,
                9: 5,
                10: 5,
                11: 6,
                12: 6,
            }
            para_time = {
                1: ('08:00', '08:45'),
                2: ('09:05', '09:50'),
                3: ('10:00', '10:45'),
                4: ('11:05', '11:50'),
                5: ('12:15', '13:00'),
                6: ('13:10', '13:55'),
                7: ('14:15', '15:00'),
                8: ('15:10', '15:55'),
                9: ('16:05', '16:50'),
                10: ('17:00', '17:45'),
                11: ('17:55', '18:40'),
                12: ('18:50', '19:35'),
            }
            data = data
            result = {}

            for i in data:
                result[i['Дата'].split(' ')[0]] = []
                for j in data:
                    if i['Дата'] == j['Дата']:
                        jj = {}
                        for kk in j:
                            if kk != 'Дата':
                                jj[kk] = j[kk]
                        result[i['Дата'].split(' ')[0]].append(jj)
            for i in result.keys():

                for j in range(0, len(result[i])):
                    result[i][j]['Пара'] = para[int(result[i][j]['UF_PARA'])]
                    result[i][j]['Время'] = para_time[int(result[i][j]['UF_PARA'])]

            for i in result.keys():
                result[i] = sorted(result[i], key=lambda item: int(item['UF_PARA']))
            for i in result.keys():
                for j in range(0, len(result[i])):
                    del result[i][j]['UF_PARA']

            return result

    def query(self, server_url: str = "", day: bool = False):

        """
        Отправка запроса на сервера колледжа;
        Входные пеараметры:
                url : str - url api колледжа

        Выходные параметры:
            Успех:
                {
                    "data": РАСПИСАНИЕ,
                    "result": True
                }
            Ошибка:
                {
                    "result": False,
                    "error": "текст ошибки"
                }

        """
        if server_url == "":
            server_url = self.server_url
        xml = """
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sch="http://www.neftpk.ru/Schedule">
            <soap:Header/>
            <soap:Body>
                <sch:Operation>
                    <sch:ID_GROUP>{0}</sch:ID_GROUP>
                    <sch:Date>{1}</sch:Date>
                </sch:Operation>
            </soap:Body>
        </soap:Envelope>
        """.format(self.group_id, self.date).encode()
        headers = {
            "Authorization": "Basic V1NOUEs6V1NOUEs="
        }
        res = self.requests.post(
            server_url, data=xml, headers=headers)

        data = self.xmltodict.parse(res.text, encoding='utf-8')
        try:
            data = data['soap:Envelope']['soap:Body']['m:OperationResponse']['m:return']['m:Tab']
        except:
            if data['soap:Envelope']['soap:Body']['m:OperationResponse']['m:return']:
                return {
                    "result": False,
                    "error": "no Schedule",
                    "request": {
                        "group_id": self.date,
                        "date": self.group_id
                    }
                }
        data = self.conveyor(data)
        weekday = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        }
        weekday_ru = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'
        }
        weekdays = {}
        for i in data.data.keys():
            weekdays[i] = {
                "en": weekday[self.datetime.datetime.strptime(i, '%d.%m.%Y').weekday()],
                "ru": weekday_ru[self.datetime.datetime.strptime(i, '%d.%m.%Y').weekday()]
            }

        try:
            if day:
                return {
                    "data": data.data[self.date],
                    "result": True,
                    "weekdays": weekdays[self.date],
                    "request": {
                        "group_id": self.date,
                        "date": self.group_id
                    }
                }
            else:
                return {
                    "data": data.data,
                    "result": True,
                    "weekdays": weekdays,
                    "request": {
                        "group_id": self.date,
                        "date": self.group_id
                    }
                }
        except TypeError:
            if not (self.regex.search(self.regular_data, self.date)):
                return {
                    "result": False,
                    "error": "wrong date",
                    "request": {
                        "group_id": self.date,
                        "date": self.group_id
                    }
                }

    def day(self, data: dict):
        """
        Метод для получения на день:
            входные параметры:
                data : dict = {
                        "group_id": GROUP,          // пример 'ИС 2.20'
                        "date": DATE                // пример '31.10.22'
                        }
        """
        self.group_id = data['group_id']
        self.date = data['date']

        return self.query(self.server_url, day=True)

    def week(self, data: dict):
        self.group_id = data['group_id']
        self.date = data['date']
        """
                Метод для получения расписания на неделю:
                    входные параметры:
                        data : dict = {
                                "group_id": GROUP,          // пример 'ИС 2.20'
                                "date": DATE                // пример '31.10.22'
                                }
                """
        return self.query(self.server_url)

if __name__ == "__main__":
    url = "http://m.neftpk.ru/college/ws/Schedule.1cws"
    print(Query(url).day({
        "group_id":"ИС 2.20",
        "date":"28.10.2022"
    })
    )