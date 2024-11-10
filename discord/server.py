from status import Status, set_status
from bot import set_bot_presence

from flask import Flask, request

import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/set-status/<status>", methods=["PUT"])
async def set_bot_status(status: str):
    if not status in ("ok", "na", "ko"):
        return "ko"
    set_status((Status.OK, Status.NA, Status.KO)[("ok", "na", "ko").index(status)])
    await set_bot_presence()
    return "ok"

@app.route("/")
def analytics():
    return "todo"

def run():
    app.run(host="0.0.0.0", port=80, debug=False)