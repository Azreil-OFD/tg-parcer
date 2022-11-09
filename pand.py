import pandas as PL
from tabulate import tabulate
import dataframe_image as dfi
from query import (Query)


def week_generate(data : dict):
    url = "http://m.neftpk.ru/college/ws/Schedule.1cws"
    data = Query(url).week(data)
    day = {'Наименование': [], 'Преподаватель': [],
           'Кабинет': [], 'Пара': [], 'Время': [], }
    days = {}
    for i in data['data']:
        for s in data['data'][i]:
            pars = []
            for asg in s:
                if (asg == 'Блок'):
                    continue
                day[asg].append(s[asg])
        days[data['request']['date'] + '_' +
             i] = PL.DataFrame(day, index=day['Пара'])
        day = {'Наименование': [], 'Преподаватель': [],
               'Кабинет': [], 'Пара': [], 'Время': [], }
    fl_names = []
    for i in days:
        del days[i]['Пара']
        filename = 'week_' + i+'.png'
        dfi.export(days[i], filename)
        fl_names.append(filename)
    return fl_names


def day_generate(data : dict):
    url = "http://m.neftpk.ru/college/ws/Schedule.1cws"
    data = Query(url).day(data)
    day = {'Наименование': [], 'Преподаватель': [],
           'Кабинет': [], 'Пара': [], 'Время': [], }
    days = {}
    if 1 == 1:
        for s in data['data']:
            pars = []
            for asg in s:
                if (asg == 'Блок'):
                    continue
                day[asg].append(s[asg])
        days[data['request']['date'] + '_' +data['request']['group_id']] = PL.DataFrame(day, index=day['Пара'])
        day = {'Наименование': [], 'Преподаватель': [],
               'Кабинет': [], 'Пара': [], 'Время': [], }

    fl_names = []
    for i in days:
        del days[i]['Пара']
        filename = 'week_' + i+'.png'
        dfi.export(days[i], filename)
        fl_names.append(filename)
    return fl_names