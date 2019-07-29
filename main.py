#! /usr/bin/python3
#  -*- coding: UTF-8 -*-
# https://dev.1c-bitrix.ru/rest_help/tasks/fields.php

from flask import Flask, request
from datetime import datetime
import requests
import const

app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    try:
        b24_token = b24token()
        id_task = request.form['data[FIELDS_AFTER][ID]']
        print(id_task)
        task = requests.post(const.b24_url_task_get, data={'taskId': id_task, 'auth': b24_token}).json()

        title = task['result']['TITLE']
        created = task['result']['CREATED_BY']
        responsible_id = task['result']['RESPONSIBLE_ID']
        responsible = task['result']['RESPONSIBLE_NAME'] + ' ' + task['result']['RESPONSIBLE_LAST_NAME']

        if task['result']['DEADLINE'] == '':
            d_line = 'срок не указан'
        else:
            d_line = datetime.strptime(task['result']['DEADLINE'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y %H:%M:%S")

        priority = task['result']['PRIORITY']
        director = task['result']['CREATED_BY_NAME'] + ' ' + task['result']['CREATED_BY_LAST_NAME']
        t_url = const.b24_url_task_view + responsible_id + '/tasks/task/view/' + id_task + '/'

        if created == responsible_id:
            return 'постановщик = ответственный'
        else:
            tlgrm_id = search_tlgrm_id(task['result']['RESPONSIBLE_ID'])
            if tlgrm_id in const.users:
                if priority == '2':
                    msg = {'chat_id': tlgrm_id,
                           'text': '📝 🔥 ' + title + '\n\n' + '✍ ' + director + '\n' + '⏰ ' + d_line + '\n' + '👀 '
                                   + '[Задача № ' + id_task + ']' + '(' + t_url + ')', 'parse_mode': 'Markdown'}
                else:
                    msg = {'chat_id': tlgrm_id,
                           'text': '📝 ' + title + '\n\n' + '✍ ' + director + '\n' + '⏰ ' + d_line + '\n' + '👀 '
                                   + '[Задача № ' + id_task + ']' + '(' + t_url + ')', 'parse_mode': 'Markdown'}

                requests.post(const.tlgrm_url, data=msg, proxies=const.proxy)
                return 'OK'
            else:
                msg = {'chat_id': const.admin,
                       'text': '[❕ ' + responsible_id + ']' + '(' + const.b24_url_user + responsible_id + '/' + ')' +
                               ' не сопоставлен с Telegram', 'parse_mode': 'Markdown'}
                requests.post(const.tlgrm_url, data=msg, proxies=const.proxy)

                msg_b24_im = {'to': created, 'message': '❕ ' + responsible + ' не имеет сопоставления с Telegram',
                              'auth': b24_token}
                requests.post(const.b24_url_im, data=msg_b24_im)
                return 'OK'

    except Exception as error:
        msg = {'chat_id': const.admin, 'text': '❗ ошибка отправки уведомления Б24\n' + str(error)}
        requests.post(const.tlgrm_url, data=msg, proxies=const.proxy)
        return 'Error'


def b24token():
    b24_token = requests.post(const.b24_oauth_token).json()['access_token']
    return b24_token


def search_tlgrm_id(responsible_id):
    for k, v in const.users.items():
        if const.users[k]['responsible_id'] == str(responsible_id):
            return k


if __name__ == '__main__':
    app.run(host='%IP%')
