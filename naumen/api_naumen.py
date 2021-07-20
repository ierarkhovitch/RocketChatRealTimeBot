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
find_service_method = "find/serviceCall$ocsservicecall/"

url = settings.URL_NAUMEN
key = settings.NAUMEN_TOKEN

find_attrs_team = {"title": "Технические специалисты спб"}
find_attrs_service = {"massProblem": "True", "state": "registered"}
find_attrs_service_ = {"massProblem": "True", "state": ["registered", "inprogress"]}


def find_user(username, ticket):
    request_find_user = f"{url}{find_user_method}%7Blogin:{username}@ocs.ru%7D?{key}"
    read_request_find_user = json.loads(requests.get(request_find_user, verify=False).text)
    if read_request_find_user:
        user_param = {"login": read_request_find_user[0]["login"],
                      "employee": read_request_find_user[0]["UUID"],
                      "ou": read_request_find_user[0]["parent"]["UUID"]}
        pprint(user_param)
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
    pprint(request_create_order)
    try:
        read_request_create_order = json.loads(requests.get(request_create_order, verify=False).text)
        pprint(read_request_create_order)
        return f"Создана заявка №{read_request_create_order['number']}"
    except:
        return "Не удалось создать заявку"


def find_service():
    request_find_service = f"{url}{find_service_method}{str(find_attrs_service)}?{key}"
    read_request_find_user = json.loads(requests.get(request_find_service, verify=False).text)
    return read_request_find_user


def find_user_tickets(username):
    find_attrs_user = {"clientEmail": [f"{username}@ocs.ru", f"{username}@lenmix.com", f"{username}@lenmixclub.com"],
                       "state": ["registered", "inprogress"]}
    request_find_tickets = f"{url}{find_service_method}{str(find_attrs_user)}?{key}"
    read_request_find_tickets = json.loads(requests.get(request_find_tickets, verify=False).text)
    tickets = []
    for ticket in read_request_find_tickets:
        if ticket['state'] == "registered":
            ticket_status = "Зарегистирована"
        elif ticket['state'] == "inprogress":
            ticket_status = "В работе"
        tickets.append(f"Номер заявки: {ticket['number']}. Статус: {ticket_status}. "
                       f"Ответсвенный: {ticket['cResponsiblle']}. Описание: {ticket['shortDescr']}")
    return tickets


# find_user_tickets('vklimov')


def find_accidents(username):
    request_find_service = f"{url}{find_service_method}{str(find_attrs_service_)}?{key}"
    read_request_find_accidents = json.loads(requests.get(request_find_service, verify=False).text)
    accidents = []
    for ticket in read_request_find_accidents:
        accidents.append(f"Номер аварии: {ticket['number']}, Описание: {ticket['shortDescr']}")
    return accidents


# find_user_tickets()

