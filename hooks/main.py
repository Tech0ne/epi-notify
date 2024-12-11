from flask import Flask, request, Response, redirect

from models import User, Hook, Method
from db import session

from login import login

from remove_expired_links import scheduler

import hashlib
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hooks are up and running"

@app.route("/hooks/<hook_id>", methods=["GET"])
def hook(hook_id):
    global session
    hook = session.query(Hook).filter_by(short_url=hook_id).first()
    if not hook:
        return Response("Hook not found, or expired", 404)
    user = hook.user

    if hook.is_redirect:
        return redirect(hook.url)

    s = login(user.token)

    try:
        s.request(hook.method.name, url=hook.url, data=hook.body)
    except Exception as e:
        return f"Error querying the page: {e}"

    session.delete(hook)
    session.commit()

    return "Done !<br>You can now close this tab !"

@app.route("/add-hook", methods=["POST"])
def add_hook():
    global session
    content = request.json
    for field, _type in {"user_id": int,
                        "method": str,
                        "url": str,
                        "body": str}.items():
        if type(content.get(field)) != _type:
            return Response("Missing required fields", 400)
    session.commit()
    user = session.query(User).filter_by(id=content.get("user_id")).first()
    if not user:
        return {"status": "error", "message": f"Could not find user with id \"{content.get('user_id')}\""}
    short_url = hashlib.md5(os.urandom(16)).hexdigest()
    hook = session.query(Hook).filter_by(short_url=short_url).first()
    while hook is not None:
        short_url = hashlib.md5(os.urandom(16)).hexdigest()
        hook = session.query(Hook).filter_by(short_url=short_url).first()
    new_hook = Hook(
        short_url=short_url,
        method=Method.from_str(content.get("method")),
        url=content.get("url"),
        body=content.get("body"),
    )

    user.hooks.append(new_hook)

    # session.add(new_hook)
    session.commit()

    return short_url

def main():
    global scheduler
    scheduler.start()
    app.run(host="0.0.0.0", port=80, debug=False)

if __name__ == "__main__":
    main()