import json, os, time
from time import sleep
from rauth import OAuth2Service
from rauth import OAuth2Session

def mkdir_p(folder):
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

def rm_f(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


# retrieve_txt(json_file_name, what_we_want_as_txt, where_we_get_the_info)
# Example usage:
#
#   retrieve(
#       json_file_name = "users_57131_scale_teams.json",
#       where = ["team", "project_gitlab_path"],
#       what = ["questions_with_answers","guidelines"],
#       title = "name"
#   )
#

def retrieve_txt(json_file_name, where, what, title=None): # what must be len=2 for now

    BASEDIR="evals/"
    with open(json_file_name) as json_file:
        json_datas = json.load(json_file)

    for data in json_datas:

        # Name of the file we will put things in. ex: "pedago_world/42-cursus/inner-circle/libft"
        file_name = data
        for i in range(len(where)):
            file_name = file_name[where[i]]

        if not file_name:
            continue
        # we take only the last part of this name. ex: folder = inner-circle, file = libft.txt
        folder, file_name = file_name.split('/')[-2:]
        file_name += "txt"
        mkdir_p(BASEDIR + folder)

        with open(BASEDIR + folder + '/' + file_name,"w+") as f:
            for i, main_content in enumerate(data[what[0]]):
                if title:
                    f.write(str(i) + ") " + main_content[title] + "\n\n")
                f.write(main_content[what[1]] + "\n\n")
    

def retrieve_json(session, path):

    mkdir_p('/'.join(path.split('/')[:-1]))
    rm_f(path + ".json")

    with open(path + ".json", "a") as json_file:

        content = []
        for number in range( 0, 100 ) :
            
            time.sleep(0.6) # please dont sleep less than 0.5 for the server limit

            web_page = session.get(f'https://api.intra.42.fr/v2/{path}?page[number]={number}', params={'format': 'json'})
            
            # Print the status once in a while
            if number % 10 == 0:
                print("Status code:", web_page.status_code)

            tmp = eval(str(web_page.json()))
            if tmp == []:
                time.sleep(0.6)
                break

            content.extend(tmp)

        json.dump(content, json_file, indent=4)


def retrieve_id(json_file_name, name, expected):
        
    with open(json_file_name) as json_file:
        json_datas = json.load(json_file)

    for data in json_datas:
        if (data[name] == expected):
            return (data["id"])



class OAuth42:

    def __init__(self):
        self.client_id = "4c8b6090c10edd4d18bfe036d2ddaacffd63beb223edecdb761d7ebcf0ed7edd"
        self.client_secret = "61685f90ae7ec137cb916dd785cf3d7252dbfd13007d21ead5ff9c150d72f4d5"
        self.service = OAuth2Service(
            name="testing",
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url="https://api.intra.42.fr/oauth/token",
            authorize_url="https://api.intra.42.fr/oauth/authorize",
            base_url="https://api.intra.42.fr/",
        )
        self.grant_type = "client_credentials"
        self.session = None
        self.token = None

    def access_token(self):
        data = {
            'client_id': self.client_id,
            'redirect_uri': 'http://google.com',
            'response_type': 'code',
            'scope': 'projects public',
            'state': 'kqmapwixucbrf2'
            }
        url = self.service.get_authorize_url(**data)
        print("\033[35m", url, "\033[m", sep='')
        code = input(f"please follow the link above and copy paste the result after 'code=' from the searchbar:\n")
        data = {
            'code': code,
            'scope': 'projects public',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://google.com/',
            'state': 'kqmapwixucbrf2'
        }
        print("result =", code)

        self.token = self.service.get_access_token(data=data)
        print("raw–token", self.token)
        return self.token

    def get_session(self):
        self.session = OAuth2Session(self.client_id, self.client_secret, access_token = self.token)
        return self.session


#      _             _   
#  ___| |_ __ _ _ __| |_ 
# / __| __/ _` | '__| __|
# \__ \ || (_| | |  | |_ 
# |___/\__\__,_|_|   \__|
#                        
# Infos about the usage of the API on https://api.intra.42.fr/apidoc


# Before trying to retrieve anything :
connection = OAuth42()
connection.access_token()
session = connection.get_session()

CAMPUS = "Brussels"
USER = "agossuin"


# campus.json
if not os.path.isfile(f"campus.json"):
    retrieve_json(session, "campus")

campus_id = retrieve_id("campus.json", "name", CAMPUS.title())
print("campus_id is", campus_id)


# campus/{campus_id}/users.json
# For big campusses, you might be waiting for up to 3 minutes...
if not os.path.isfile(f"campus/{campus_id}/users.json"):
    retrieve_json(session, f"campus/{campus_id}/users")

user_id = retrieve_id(f"campus/{campus_id}/users.json", "login", USER)
print("user_id is", user_id)


# users/{user_id}/scale_teams + retrieving evals
if not os.path.isfile(f"users/{user_id}/scale_teams.json"):
    retrieve_json(session, f"users/{user_id}/scale_teams")
retrieve_txt(f"users/{user_id}/scale_teams.json", where=["team", "project_gitlab_path"], what=["questions_with_answers","guidelines"], title = "name")

# Slots
# if not os.path.isfile(f"projects/1342/slots"):
retrieve_json(session, f"projects/1342/slots")
