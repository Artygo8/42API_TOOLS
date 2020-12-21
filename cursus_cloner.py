import os, json
from OAuth42 import OAuth42, mkdir_p, rm_f # import the class from the file
from git import Repo # pip install gitpython

connection = OAuth42()

CAMPUS = ""
USER = ""

if CAMPUS == "": CAMPUS = input("What is your campus? ")
if USER == "": USER = input("What is your username? ")


# GET CAMPUS
if not os.path.isfile(f"campus.json"):
    connection.get_json_basic("campus")

with open("campus.json") as campus_json:
    for campus in json.load(campus_json):
        if campus["name"].upper() == CAMPUS.upper():
            campus_id = campus["id"]
            break

print("campus_id is", campus_id)


# GET USER ID
if not os.path.isfile(f"campus/{campus_id}/users.json"):
    connection.get_json_basic(f"campus/{campus_id}/users")

with open(f"campus/{campus_id}/users.json") as campus_users_json:
    for users in json.load(campus_users_json):
        if users["login"].upper() == USER.upper():
            user_id = users["id"]
            break

print("user_id is", user_id)


# GET REPOSITORIES
if not os.path.isfile(f"users/{user_id}/projects_users.json"):
    connection.get_json_basic(f"users/{user_id}/projects_users")

with open(f"users/{user_id}/projects_users.json") as projects:
    for project in json.load(projects):
        for team in project["teams"]:
            if team["validated?"]:
                if team["project_gitlab_path"] and not os.path.exists(team["project_gitlab_path"]):
                    print("cloning", team["project_gitlab_path"].split('/')[-1])
                    Repo.clone_from(team["repo_url"], team["project_gitlab_path"])

print("DONE!")
