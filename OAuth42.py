import json, os, requests, chime
from time import sleep

#  _              _     
# | |_ ___   ___ | |___ 
# | __/ _ \ / _ \| / __|
# | || (_) | (_) | \__ \
#  \__\___/ \___/|_|___/
#                       

def mkdir_p(folder):
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

def rm_f(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)

#   ___    _         _   _     _  _  ____  
# /  _  \ / \  _   _| |_| |__ | || ||___  \ 
# | | | |/ _ \| | | | __| '_ \| || |_ __/ |
# | |_| / ___ \ |_| | |_| | | |__   _/ __/ 
# \____/_/   \_\__,_|\__|_| |_|  |_||_____|
#                                          

class OAuth42:

        def __init__(self):
            chime.theme('mario')
            with open("credentials.json") as creds:
                json_cred = json.load(creds)
                self.client_id = json_cred["client_id"]
                self.client_secret = json_cred["client_secret"]
                self.redirect_uri = json_cred["redirect_uri"]
            self.authorize_url = "https://api.intra.42.fr/oauth/authorize"
            self.access_token_url = "https://api.intra.42.fr/oauth/token"
            self.base_url = "https://api.intra.42.fr/v2"
            self.public_token = None
            self.access_token = None
            self.refresh_token = None
            self.code = None

        #  ,               ,      
        # | |,,   ,, , ,,,(,) ,,, 
        # | ', \ / ,` / ,,| |/ ,,|
        # | |,) | (,| \,, \ | (,, 
        # |,.,,/ \,,,,|,,,/,|\,,,|
        #                         

        def get_basic_access(self):
            post_data = {
                'grant_type' : "client_credentials",
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
            }
            response = requests.post(self.access_token_url, data=post_data)
            json_response = response.json()
            try:
                self.public_token = json_response["access_token"]
            except:
                chime.error()
                exit("cannot get basic access")


        def get_json_basic(self, path, max_nb_page=1000, basedir="./", show_status_code=False):

            if not self.public_token: self.get_basic_access()

            path = basedir + path
            mkdir_p('/'.join(path.split('/')[:-1]))
            rm_f(path + ".json")

            with open(path + ".json", "w") as json_file:

                content = []
                for page_number in range(0, max_nb_page):
            
                    print("page_number", page_number)

                    sleep(0.6) # Please dont sleep less than 0.5 for the server limit.

                    response = requests.get(f'{self.base_url}/{path}?page={page_number}', headers = {"Authorization": f"Bearer {self.public_token}"})

                    if response.status_code >= 400:
                        rm_f(path + ".json")
                        chime.error()
                        exit(f"something went wrong... {response.reason} {response.status_code}")
                        return

                    tmp = eval(str(response.json()))
                    if tmp == []:
                        break

                    content.extend(tmp)

                json.dump(content, json_file, indent=4)

        #   ,, ,               
        #  / ,| | ,,,,,      ,,
        # | |,| |/ , \ \ /\ / /
        # |  ,| | (,) \ V  V / 
        # |,| |,|\,,,/ \,/\,/  

        def refresh_access_token(self):
            post_data = {
                'grant_type' : "refresh_token",
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'refresh_token' : self.refresh_token,
                'scope' : "public projects"
            }
            response = requests.post(self.access_token_url, data=post_data)
            print(f"response = ({response.status_code}) {response.content}")
            json_response = response.json()
            try:
                self.access_token = json_response["access_token"]
            except:
                chime.error()
                exit("cannot refresh access token")
            return self.access_token

        def get_access_token(self):

            if self.refresh_token:
                self.refresh_access_token()
                return
            chime.success()
            print(f"https://api.intra.42.fr/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope=public%20projects") # no state for now.
            self.code = input("Paste the code from the url: ")
            post_data = {
                'grant_type' : "authorization_code",
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'code' : self.code,
                'redirect_uri' : "https://www.google.com/"
            }
            response = requests.post(self.access_token_url, data=post_data)
            print(f"response = ({response.status_code}) {response.content}")
            json_response = response.json()
            try:
                self.access_token = json_response["access_token"]
                self.refresh_token = json_response["refresh_token"]
            except:
                chime.error()
                exit("cannot retrieve access token")
            return self.access_token

        def get_json_restricted(self, path, max_nb_page=1000, basedir="./", show_status_code=False):

            path = basedir + path
            mkdir_p('/'.join(path.split('/')[:-1]))
            rm_f(path + ".json")

            with open(path + ".json", "w+") as json_file:

                content = []
                for page_number in range(0, max_nb_page):

                    sleep(1) # Please dont sleep less than 0.5 for the server limit, I use 1 so we can have more than one user at the time. + it shouldnt be more than 2 pages anyway

                    response = requests.get(f'{self.base_url}/{path}?page[number]={page_number}', headers = {"Authorization": f"Bearer {self.access_token}"})

                    if show_status_code: print("status:", response.status_code)

                    if response.status_code >= 400:
                        rm_f(path + ".json")
                        if response.status_code == 401:
                            self.get_access_token()
                            break
                        chime.error()
                        exit(f"something went wrong... {response.reason} {response.status_code}")

                    tmp = eval(str(response.json()))
                    if tmp == []:
                        break

                    content.extend(tmp)

                json.dump(content, json_file, indent=4)
