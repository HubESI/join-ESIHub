import os
import flask
from flask import Flask, abort
from flask_cors import CORS
from config import INV_TEAM, JOIN_ESI_HUB_GP_LINK
from github_api_ops import get_token, get_user_emails, get_user_info, get_team_id, invite_user

app = Flask(__name__)
CORS(app, ressources={r'*': {'origins': ['https://hubesi.github.io']}})

def get_esi_email(emails):
    for email_dict in emails:
        if email_dict["email"].split("@")[1] == "esi.dz":
            return email_dict

@app.route("/")
def hello():
    return flask.redirect(JOIN_ESI_HUB_GP_LINK)

@app.route("/check")
def check_invite():
    if "code" not in flask.request.args:
        abort(400)
    code = flask.request.args.get("code")
    token = get_token(code)
    user_emails = get_user_emails(token)
    esi_email = get_esi_email(user_emails)
    if esi_email is None:
        return {
            "success": False,
            "error": "Missing email",
            "description": "To join ESIHub org you must add your @esi.dz email \
to your Github account"
        }
    if not esi_email["verified"]:
        return {
            "success": False,
            "error": "Email not verified",
            "description": "Your @esi.dz email is not verified in your Github account, \
please verify it so you can join"
        }
    pat = os.environ["ORG_PAT"]
    team_id = get_team_id(pat, INV_TEAM)
    invite_user(pat, get_user_info(token)['id'], [team_id])
    return {
        "success": True,
        "description": "An invitation to join the org has been sent to you"
    }
