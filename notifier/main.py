# from .login import login

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from threading import Lock

from models import User, Method #, Hook
from db import session

from login import login

import requests
import datetime
import asyncio
import signal
import fcntl
import time
import json
import sys
import os

# SLEEP_TIME = 60 * 30
SLEEP_TIME = 60 * 1

current_events = {}
registered_events = []

class Event:
# {
#   'scolaryear': '2024',
#   'codemodule': 'G-GPR-000',
#   'codeinstance': 'NCE-0-1',
#   'codeacti': 'acti-655471',
#   'codeevent': 'event-592340',
#   'semester': 0,
#   'instance_location': 'FR/NCE',
#   'titlemodule': 'G0 - Free Coaching',
#   'prof_inst': [{'type': 'user',
#       'login': 'fanny.parola@epitech.eu',
#       'title': 'Fanny Parola',
#       'picture': '/file/userprofil/fanny.parola.bmp'}],
#   'acti_title': 'Coaching Session. Tech 3',
#   'num_event': 1,
#   'start': '2024-10-29 09:30:00',
#   'end': '2024-10-29 17:30:00',
#   'total_students_registered': 0,
#   'title': None,
#   'type_title': 'Follow-up',
#   'type_code': 'rdv',
#   'is_rdv': '1',
#   'nb_hours': '08:00:00',
#   'allowed_planning_start': '2024-09-24 00:00:00',
#   'allowed_planning_end': '2025-02-28 00:00:00',
#   'nb_group': 1,
#   'nb_max_students_projet': None,
#   'room': {'code': 'FR/NCE/Epitech-Les-Cimes/Stephen-Hawking',
#       'type': 'salle-de-reunion',
#       'seats': 6},
#   'dates': None,
#   'module_available': True,
#   'module_registered': True,
#   'past': False,
#   'allow_register': False,
#   'event_registered': False,
#   'display': '0',
#   'project': False,
#   'rdv_group_registered': None,
#   'rdv_indiv_registered': None,
#   'allow_token': False,
#   'register_student': True,
#   'register_prof': False,
#   'register_month': False,
#   'in_more_than_one_month': False
# }

    def __init__(self, user_id: int, ping_time: str, event: dict, message: str, register_action: dict = None):
        self.date = datetime.datetime.strptime(event.get("start"), "%Y-%m-%d %H:%M:%S") - datetime.timedelta(seconds=ping_time)
        self.user_id = user_id
        self.id = f"{event.get('codeevent')}-{round(self.date.timestamp())}-{user_id}"
        self.args = (self.user_id, {
            "message": "",
            "embed": {
                "title": "EpiNotify - Intra notification",
                "description": message,
                "color": 3452386,
                "fields": [
                    {
                        "name": "Intranet reminder",
                        "value": "You got an intranet event !",
                    }
                ]
            },
            "ntfy": {
                "message": message,
            }
        })
        self.is_rdv = bool(event.get("is_rdv"))
        #             \/  : Doesn't support rdv events as of rn. This is bcause it's fkin anoying to manage
        if not self.is_rdv and register_action is not None:
            self.args[1]["ntfy"]["actions"] = [register_action]

def ping_back(user_id: int, message: dict):
    req = requests.post(f"http://bot/send-event/{user_id}", json=message).content

def get_register_url(event):
    #                                                                                Sry bout that  \/
    return f"https://intra.epitech.eu/module/{event.get('scolaryear')}/{event.get('codemodule')}/NCE-5-1/{event.get('codeacti')}/{event.get('codeevent')}/register?format=json"

def retreive_all_events(user_id: int, token: str):
    s = login(token)

    today = datetime.date.today()
    weekday = today.weekday()
    st = (today + datetime.timedelta(days=7 - weekday)) if weekday in (5, 6) else today - datetime.timedelta(days=weekday)
    nd = st + datetime.timedelta(days=7)
    events = s.get(f"https://intra.epitech.eu/planning/load?format=json&start={st}&end={nd}")
    if events.status_code != 200:
        print(f"[ERROR] Got status code {events.status_code} while fetching the intranet !", file=sys.stderr)
    all_events = []
    for event in events.json():
        # Add event 5 days before when not logged in
        if not event.get("event_registered"):
            all_events.append(Event(user_id, 3 * 24 * 60 * 60, event, "You are not registered to the intranet event !", {
                "action": "http",
                "label": "Register",
                "url": get_register_url(event),
                "method": "POST",
                "headers": {
                    "Cookie": '; '.join([f"{k}={v}" for k, v in s.cookies.items()])
                }
            }))
        # Add event 1 day before
        all_events.append(Event(user_id, 24 * 60 * 60, event, "You have an intranet event in 1 day !"))
        # Add event 1 hour before
        all_events.append(Event(user_id, 60 * 60, event, "You have an intranet event in 1 hour !"))
        # Add event 10 minutes before
        all_events.append(Event(user_id, 60 * 60, event, "You have an intranet event in 10 minutes !"))
    return all_events

def register_new_tasks(scheduler):
    session.commit()
    for user in session.query(User).filter(User.token != None).all():
        session.commit()
        for event in retreive_all_events(user.id, user.token)[:1]:
            current_events.update({event.id: event})
            if not event.id in registered_events:
                scheduler.add_job(
                    ping_back,
                    trigger=DateTrigger(run_date=event.date),
                    args=event.args,
                    id=event.id,
                )
                registered_events.append(event.id)

def main() -> int:
    # Initial timeout: DB help + wait for bot to be good
    time.sleep(5)
    scheduler = BackgroundScheduler()
    scheduler.start()
    try:
        while True:
            register_new_tasks(scheduler)
            time.sleep(SLEEP_TIME)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())