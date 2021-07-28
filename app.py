import os
import flask
from flask import Flask
import requests
import json

app = Flask(__name__)

GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API = "https://api.github.com"
ORG_LOGIN = "HubESI"
ESIHUB_LINK = f"https://github.com/{ORG_LOGIN}"
INV_TEAM = "base-team"

def get_token(code):
    body = json.dumps({
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "code": code,
        "redirect_uri": "{}/check".format(os.environ["APP_URL"])
    })
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.request("POST", GITHUB_TOKEN_URL, headers=headers, data=body)
    return response.json()["access_token"]

def get_user_info(token):
    url = f"{GITHUB_API}/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def get_team_id(pat, team_slug):
    url = f"{GITHUB_API}/orgs/{ORG_LOGIN}/teams/{team_slug}"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()['id']


def invite_user(pat, user_id, teams_ids):
    url = f"{GITHUB_API}/orgs/{ORG_LOGIN}/invitations"
    body = json.dumps({
        "invitee_id": user_id,
        "team_ids": teams_ids
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.request("POST", url, headers=headers, data=body)
    return response.json()


@app.route("/")
def hello():
    return flask.redirect(ESIHUB_LINK)

@app.route("/check")
def check_invite():
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
