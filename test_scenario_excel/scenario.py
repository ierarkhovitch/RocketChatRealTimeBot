# -*- coding: utf-8 -*-

from pprint import pprint
import json
import os

import pandas as pd


def init_buttons(path):
    buttons = dict()
    file = pd.read_excel(path, sheet_name='buttons')
    for index, row in file.iterrows():
        row = dict(row)
        button = str(row['text'])
        row['type'], row['msg_in_chat_window'], row['msg'] = "button", True, row['text']
        if isinstance(row['url'], float):
            row.pop('url')
        if isinstance(row['scenario'], float):
            row.pop('scenario')
            row.pop('msg')
            row.pop('msg_in_chat_window')
        buttons[button] = row
    return buttons

# pprint(init_buttons('scenario.xlsx'))


def init_scene(path):
    buttons = init_buttons(path)
    scenario_msg = dict()
    file = pd.read_excel(path, sheet_name='scenario')
    for index, row in file.iterrows():
        row = dict(row)
        if isinstance(row['text'], float):
            row.pop('text')
        scenario = row['description']
        row.pop('description')
        buttons_scenario_id = row['actions'].split(';')
        buttons_scenario = []
        for button in buttons_scenario_id:
            buttons_scenario.append(buttons[button])
        row['actions'] = buttons_scenario
        row['color'] = "#73b6ce"
        scenario_msg[scenario] = row
    return scenario_msg


# pprint(init_scene(path='scenario.xlsx'))


