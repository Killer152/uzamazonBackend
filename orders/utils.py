import base64
import json
import logging
import random
import string
import datetime

import requests
from django.conf import settings


logger = logging.getLogger(__file__)


def get_sms_json_template(phone, text, sms_id):
    d = "[{'phone':'" + phone + "', 'text':'" + text + "'}]"
    data = {
        'login': settings.SMS_LOGIN,
        'password': settings.SMS_PASS,
        'data': d
    }
    return data


def send_sms(data):
    # text = settings.SMS_LOGIN + ':' + settings.SMS_PASS
    # text = text.encode('utf-8')
    # encoded = base64.b64encode(text)
    # encoded = encoded.decode('utf-8')
    #
    # headers = {
    #     'Content-Type': "application/json",
    #     'Authorization': "Basic " + encoded,
    #     'cache-control': "no-cache",
    #     'Postman-Token': "effa6d6c-01b4-475c-8094-78b1f49c8282"
    # }
    r = requests.post(settings.SMS_URL, data=data)
    logger.error(str(datetime.datetime.now()) + '\n' + r.text)


def send_sms_code(phone, text, user_id):
    # data = get_sms_json_template(phone, text, user_id)
    d = '[{"phone":"' + phone + '", "text":"' + text + '"}]'
    data = {
        'login': 'KOINOT',
        'password': '84uiiZ27a90al7dB0cjL',
        'data': d
    }

    print(d)

    # response = requests.post('http://185.8.212.184/smsgateway/', data=data) нада
    # logger.error(str(datetime.datetime.now()) + '\n' + response.text)

    # send_sms(data)


def send_code(phone, code):
    text = 'UzAmazon'
