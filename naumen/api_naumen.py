# -*- coding: utf-8 -*-

from pprint import pprint
import json
import requests
import urllib3

import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

create_method = "create-m2m/serviceCall/"
find_user_method = "find/employee/"
find_team_method = "find/team/"
find_service_call_method = "find/serviceCall/"
find_service_method = "find/slmService/"

url = settings.URL_NAUMEN
key = settings.NAUMEN_TOKEN

# find_attrs_team = {"title": "Технические специалисты спб"}
# find_attrs_service = {"title": "Заявки:OCS"}


def find_user(username, ticket):
    request_find_user = f"{url}{find_user_method}%7Blogin:{username}@ocs.ru%7D?{key}"
    read_request_find_user = json.loads(requests.get(request_find_user, verify=False).text)
    if read_request_find_user:
        user_param = {"login": read_request_find_user[0]["login"],
                      "employee": read_request_find_user[0]["UUID"],
                      "ou": read_request_find_user[0]["parent"]["UUID"]}
    else:
        print('Пользователь не найден')
        user_param = settings.ROCKET_USER
    attributes = {"agreement": "agreement$4660001", "clientEmployee": user_param["employee"],
                  "clientOU": user_param["ou"], "descriptionRTF": ticket["text"],
                  "metaClass": "serviceCall$ocsservicecall", "responsibleTeam": settings.SUPPORT_SPB_TEAM,
                  "service": settings.SUPPORT_SPB_SERVICE, "shortDescr": ticket["theme"], "wayAddressing": "api"}
    return attributes


def create_order(username, ticket):
    attributes = find_user(username, ticket)
    request_create_order = f"{url}{create_method}{str(attributes)}?{key}"
    try:
        read_request_create_order = json.loads(requests.get(request_create_order, verify=False).text)
        return f"Создана заявка №{read_request_create_order['number']}"
    except:
        return "Не удалось создать заявку"


def find_team():
    request_find_team = f"{url}{find_team_method}{str(find_attrs_team)}?{key}"
    read_request_find_team = json.loads(requests.get(request_find_team, verify=False).text)
    return read_request_find_team


def find_service():
    request_find_service = f"{url}{find_service_method}{str(find_attrs_service)}?{key}"
    read_request_find_user = json.loads(requests.get(request_find_service, verify=False).text)
    return read_request_find_user

