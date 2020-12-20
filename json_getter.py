import json, os, time
from rauth import OAuth2Service
from rauth import OAuth2Session

def mkdir_p(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def rm_f(path):
    if os.path.exists(path):
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
            time.sleep(1)
            web_page = session.get(f'https://api.intra.42.fr/v2/{path}?page[number]={number}', params={'format': 'json'})
            print("Status code:", web_page.status_code)
            tmp = eval(str(web_page.json()))
            if tmp == []:
                break
            content.extend(tmp)

        json.dump(content, json_file, indent=4)


def retrieve_data(json_file_name, what, content):
    pass


class OAuth42:

    def __init__(self):
        self.client_id = "4c8b6090c10edd4d18bfe036d2ddaacffd63beb223edecdb761d7ebcf0ed7edd"
        self.client_secret="61685f90ae7ec137cb916dd785cf3d7252dbfd13007d21ead5ff9c150d72f4d5"
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
        data = {'grant_type': self.grant_type, 'redirect_uri': 'http://127.0.0.1'}

        self.token = self.service.get_auth_session(data=data, decoder=json.loads).access_token
        return self.token

    def get_session(self):
        self.session = OAuth2Session(self.client_id, self.client_secret, access_token = self.token)
        return self.session





# Before trying to retrieve anything :
connection = OAuth42()
connection.access_token()
session = connection.get_session()

retrieve_json(session, "users/57131/scale_teams")
retrieve_txt("users/57131/scale_teams.json", where=["team", "project_gitlab_path"], what=["questions_with_answers","guidelines"], title = "name")
