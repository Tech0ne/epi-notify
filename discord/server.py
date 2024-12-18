from status import Status, set_status
from bot import set_bot_presence, send_dm, send_ntfy

from flask import Flask, request

import logging
import sys

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

@app.route("/send-event/<int:user_id>", methods=["POST"])
def send_message(user_id: int):
    message = request.json.get("message")
    embed = request.json.get("embed")
    ntfy = request.json.get("ntfy")

    send_dm(user_id, message, embed)
    send_ntfy(user_id, ntfy)
    return "ok"

@app.route("/")
def analytics():
    return "todo"

def run():
    app.run(host="0.0.0.0", port=80, debug=False)