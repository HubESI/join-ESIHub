import os
from flask import Flask, redirect, request
from flask_cors import CORS
from config import INV_TEAM, JOIN_ESI_HUB_GP_LINK
from github_api_ops import get_token, get_user_emails, get_user_info, get_team_id, invite_user
from api_errors import ApiError, CheckResult, not_enough_permissions, code_not_provided, \
esi_email_not_found, esi_email_not_verified

app = Flask(__name__)
CORS(app, ressources={r'*': {'origins': ['https://hubesi.github.io']}})

def get_esi_email(emails):
    for email_dict in emails:
        if email_dict["email"].split("@")[1] == "esi.dz":
            return email_dict

@app.route("/")
def hello():
    return redirect(JOIN_ESI_HUB_GP_LINK)

@app.route("/invite")
def check_invite():
    if "code" not in request.args:
        raise code_not_provided
    code = request.args.get("code")
    token = get_token(code)
    if "error" in token:
        raise ApiError(403, token["error"], token["error_description"])
    if "user:email" not in token["scope"].split(","):
        raise not_enough_permissions
    user_emails = get_user_emails(token["access_token"])
    esi_email = get_esi_email(user_emails)
    user_info = get_user_info(token["access_token"])
    if esi_email is None:
        esi_email_not_found.gh_user = user_info["login"]
        raise esi_email_not_found
    if not esi_email["verified"]:
        esi_email_not_verified.gh_user = user_info["login"]
        raise esi_email_not_verified
    pat = os.environ["ORG_PAT"]
    team_id = get_team_id(pat, INV_TEAM)
    invite_user(pat, user_info['id'], [team_id])
    return CheckResult(
        200,
        True,
        user_info["login"],
        "An invitation to join the org has been created"
    ).to_dict(), 200

@app.errorhandler(ApiError)
def handle_apierror(e):
    return e.to_dict(), e.status_code

@app.errorhandler(CheckResult)
def handle_apierror(e):
    return e.to_dict(), e.status_code
