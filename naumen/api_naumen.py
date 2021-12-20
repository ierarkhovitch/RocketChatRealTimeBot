# -*- coding: utf-8 -*-

import json
import requests
import urllib3
import re


import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

domain = settings.DOMAIN
url = settings.URL_NAUMEN
key = settings.NAUMEN_TOKEN
service_call_prefix = settings.SERVICE_CALL_PREFIX

find_team_method = "find/team/"
find_user_method = "find/employee/"
create_method = "create-m2m/serviceCall/"
find_service_call_method = "find/serviceCall/"
find_service_method = f"find/serviceCall{service_call_prefix}/"

find_attrs_team = {"title": "Технические специалисты спб"}
find_attrs_service = {"massProblem": "True", "state": "registered"}
find_attrs_service_ = {"massProblem": "True", "state": ["registered", "inprogress"]}


def find_user(username, ticket):
    request_find_user = f"{url}{find_user_method}%7Blogin:{username}@{domain}%7D?{key}"
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
                  "metaClass": f"serviceCall${service_call_prefix}", "responsibleTeam": settings.SUPPORT_SPB_TEAM,
                  "service": settings.SUPPORT_SPB_SERVICE, "shortDescr": ticket["theme"], "wayAddressing": "api"}
    return attributes


def create_order(username, ticket):
    attributes = (find_user(username, ticket))
    request_create_order = f"{url}{create_method}{str(attributes)}?{key}"
    # print(request_create_order)
    try:
        read_request_create_order = json.loads(requests.post(request_create_order, verify=False).text)
        return f"Создана заявка №{read_request_create_order['number']}"
    except Exception as exc:
        print(exc)
        return "Не удалось создать заявку"


def find_service():
    request_find_service = f"{url}{find_service_method}{str(find_attrs_service)}?{key}"
    read_request_find_user = json.loads(requests.get(request_find_service, verify=False).text)
    return read_request_find_user


def find_user_tickets(username):
    find_attrs_user = {"clientEmail": f"{username}@{domain}",
                       "state": ["registered", "inprogress", "accepting"]}
    request_find_tickets = f"{url}{find_service_call_method}{str(find_attrs_user)}?{key}"
    read_request_find_tickets = json.loads(requests.get(request_find_tickets, verify=False).text)
    tickets = []
    for ticket in read_request_find_tickets:
        if ticket['state'] == "registered":
            ticket_status = "Зарегистирована"
        elif ticket['state'] == "inprogress":
            ticket_status = "В работе"
        elif ticket['state'] == "accepting":
            ticket_status = "На согласовании"
        else:
            ticket_status = "Активна"
        tickets.append(f"Номер заявки: {ticket['number']}. Статус: {ticket_status}. "
                       f"Ответственный: {ticket['cResponsiblle']}. Описание: {ticket['shortDescr']}\n")
    return tickets


def find_accidents(username):
    request_find_service = f"{url}{find_service_method}{str(find_attrs_service_)}?{key}"
    read_request_find_accidents = json.loads(requests.get(request_find_service, verify=False).text)
    accidents = []
    for ticket in read_request_find_accidents:
        accidents.append(f"Номер аварии: {ticket['number']}, Описание: {ticket['shortDescr']}")
    return accidents


def find_announcement(username):
    find_service_method_ = "find/catalogs$announcement/"
    # find_attrs_service1 = {"metaClass": "catalogs$announcement"}
    request_find_service = f"{url}{find_service_method_}?{key}"
    read_request_find_user = json.loads(requests.get(request_find_service, verify=False).text)
    return re.sub(r'(\<[^>]*>)|(&nbsp;)', '', read_request_find_user[0]['description']) + '\n'
