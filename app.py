import os
import flask
from flask import Flask, abort
from config import INV_TEAM, JOIN_ESI_HUB_GP_LINK
from github_api_ops import get_token, get_user_info, get_team_id, invite_user, invite_email

app = Flask(__name__)

@app.route("/")
def hello():
    return flask.redirect(JOIN_ESI_HUB_GP_LINK)

@app.route("/check")
def check_invite():
    if "code" in flask.request.args:
        code = flask.request.args.get("code")
        token = get_token(code)
        user_info = get_user_info(token)
        if user_info["email"] is None:
            return {
                "success": False,
                "error": "Missing email",
                "description": "Please make your GitHub email address public\
so we can verify that you are an ESI member"
            }
        email_domain = user_info["email"].split("@")[1]
        if email_domain != "esi.dz":
            return {
                "success": False,
                "error": "Outside ESI email",
                "description": "To join ESIHub org your GitHub email address\
must be an ESI email"
            }
        pat = os.environ["ORG_PAT"]
        team_id = get_team_id(pat, INV_TEAM)
        invite_user(pat, user_info['id'], [team_id])
        return {
            "success": True,
            "description": "An invitation to join the org has been sent to you"
        }
    elif "email" in flask.request.args:
        email = flask.request.args.get("email")
        email_domain = email.split("@")[1]
        if email_domain != "esi.dz":
            return {
                "success": False,
                "error": "Outside ESI email",
                "description": "To join ESIHub org your GitHub email address\
must be an ESI email"
            }
        pat = os.environ["ORG_PAT"]
        team_id = get_team_id(pat, INV_TEAM)
        invite_email(pat, email, [team_id])
        return {
            "success": True,
            "description": "An invitation to join the org has been sent to you"
        }
    else:
        abort(400)
