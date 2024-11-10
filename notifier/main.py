# from .login import login

from threading import Lock
import requests
import datetime
import asyncio
import signal
import fcntl
import json
import sys
import os

#region db

# User format:
# {
#   "id": "name.surname@epitech.eu",
#   "token": "[intra.epitech.eu token]",
#   "discord_uid": "[discord UID]" | None,
#   "ntfy_uri": "[Ntfy path]" | None,
#   "off_time": ([start_time], [end_time]), # Defines the time of day where notifications should be avoided. Is overwrote by max level notifications. Is defined like so: XX:XX (hour in the day)
#   "rules": {
#       "event": [
#           [RULE FORMAT]
#       ],
#       "rdv:unregistered": [
#           [RULE FORMAT]
#       ],
#       "rdv:registered": [
#           [RULE FORMAT] | "event"
#       ]
#   }
# }

# Rule format:
# {
#   "id": "[sample rule ID (like "ping_1_hour_before")]",
#   "user_id": "name.surname@epitech.eu",
#   "time": "[Time formating: XXj-XXh-XXm]"
# }

USERS = []
USERS_LOCK = Lock()

def load_db():
    global USERS
    with USERS_LOCK:
        USERS.clear()
        USERS.extend(json.load(open("/data/db.json", 'r')))

if not os.path.isfile("/data/db.json"):
    print("Could not start without database", file=sys.stderr)
    sys.exit(1)

#endregion

#region API

def get_activities(session: requests.Session, week_start: str, week_end: str):
    events_request = session.get(f"https://intra.epitech.eu/planning/load?format=json&start={week_start}&end={week_end}")
    if events_request.status_code != 200:
        raise ValueError(f"Got status code {events_request.status_code}")
    return [Event(event) for event in events_request.json()]

# /module/2024/G-GPR-000/NCE-0-1/acti-655496/rdv/?format=json

def get_rdv(session: requests.Session, ):
    pass

#endregion

#region utils

def retreive_target_week():
    today = datetime.datetime.today()
    weekday = today.weekday()

    target_date = None

    if weekday in (5, 6):
        target_date = today + datetime.timedelta(days=7 - weekday)
    else:
        target_date = today - datetime.timedelta(days=weekday)

    return (target_date.strftime("%Y-%m-%d"), (target_date + datetime.timedelta(days=7)).strftime("%Y-%m-%d"))

#endregion

class User:
    def __init__(self, **infos):
        for attr in ("id", ""):
            setattr(self, attr, infos.get(attr))

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

    def __init__(self, event: dict):
        self.is_rdv = bool(event.get("is_rdv"))

    def dump(self):
        return None

    def load(data):
        return Event()

def load_events(path: str):
    events = json.load(open(path, 'r'))
    events = [Event.load(event) for event in events]
    return events

def dump_events(events: list[Event], path: str):
    dump_events = [event.dump() for event in events]
    json.dump(dump_events, open(path, 'w+'))

def main() -> int:
    global USERS, USERS_LOCK
    signal.signal(signal.SIGIO, load_db)
    fd = os.open("/data/db.json",  os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY, fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)



    week = retreive_target_week()
    events = get_activities(session, *week)
    return 0

if __name__ == "__main__":
    sys.exit(main())