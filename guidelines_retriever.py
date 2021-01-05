import os, json
from OAuth42 import OAuth42, mkdir_p, rm_f # import the class from the file

connection = OAuth42()

CAMPUS = ""
USER = ""

if CAMPUS == "": CAMPUS = input("Where is your campus (brussels, paris, ...)? ")
if USER == "": USER = input("What is your username? ")


# GET CAMPUS
if not os.path.isfile(f"campus.json"):
    connection.get_json_basic("campus")

campus_id = 0
with open("campus.json") as campus_json:
    for campus in json.load(campus_json):
        if campus["name"].upper() == CAMPUS.upper():
            campus_id = campus["id"]
            break

print("campus_id is", campus_id)


# GET USER ID
if not os.path.isfile(f"campus/{campus_id}/users.json"):
    connection.get_json_basic(f"campus/{campus_id}/users")


user_id = 0
with open(f"campus/{campus_id}/users.json") as campus_users_json:
    for users in json.load(campus_users_json):
        if users["login"].upper() == USER.upper():
            user_id = users["id"]
            break

print("user_id is", user_id)
# if not user_id:
#     exit("user_id not found")

# RETRIEVE GUIDELINES
if not os.path.isfile(f"users/{user_id}/scale_teams.json"):
    connection.get_json_basic(f"users/{user_id}/scale_teams")

# if not os.path.isfile(f"users/{user_id}/scale_teams.json"):
#     exit()

BASEDIR="guidelines/"

with open(f"users/{user_id}/scale_teams.json") as scale_teams_json:
    teams = json.load(scale_teams_json)
    for team in teams:
        if not team["team"]["project_gitlab_path"]:
            continue
        file_name = BASEDIR + team["team"]["project_gitlab_path"] + ".txt"
        if os.path.isfile(file_name):
            continue
        mkdir_p('/'.join(file_name.split('/')[:-1]))
        with open(file_name, "w+") as f:
            for i, question in enumerate(team["questions_with_answers"]):
                f.write("\n" + str(i) + ") " + question["name"] + "\n")
                f.write(str(question["guidelines"]) + "\n\n")

print("DONE!")