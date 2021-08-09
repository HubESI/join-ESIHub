import os
import requests
import json
from config import GITHUB_TOKEN_URL, GITHUB_API, ORG_LOGIN, AUTH_CALLBACK_URL

def get_token(code):
    body = json.dumps({
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "code": code,
        "redirect_uri": AUTH_CALLBACK_URL
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

def invite_email(pat, email, teams_ids):
    url = f"{GITHUB_API}/orgs/{ORG_LOGIN}/invitations"
    body = json.dumps({
        "email": email,
        "team_ids": teams_ids
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.request("POST", url, headers=headers, data=body)
    return response.json()
