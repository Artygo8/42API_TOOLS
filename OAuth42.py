import json, os, requests, datetime
from time import sleep

def mkdir_p(folder):
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

def rm_f(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


class OAuth42:

        def __init__(self):
            self.client_id = "4c8b6090c10edd4d18bfe036d2ddaacffd63beb223edecdb761d7ebcf0ed7edd"
            self.client_secret="61685f90ae7ec137cb916dd785cf3d7252dbfd13007d21ead5ff9c150d72f4d5"
            self.authorize_url = "https://api.intra.42.fr/oauth/authorize"
            self.access_token_url = "https://api.intra.42.fr/oauth/token"
            self.base_url = "https://api.intra.42.fr/v2"
            self.public_token = None
            self.access_token = None
            self.code = None

        #  _               _      
        # | |__   __ _ ___(_) ___ 
        # | '_ \ / _` / __| |/ __|
        # | |_) | (_| \__ \ | (__ 
        # |_.__/ \__,_|___/_|\___|
        #                         

        def get_basic_access(self):
            post_data = {
                'grant_type' : "client_credentials",
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
            }
            r = requests.post(self.access_token_url, data=post_data)
            response = r.json()
            self.public_token = response["access_token"]

        def get_json_basic(self, path):

            if not self.public_token:
                self.get_basic_access()

            mkdir_p('/'.join(path.split('/')[:-1]))
            rm_f(path + ".json")

            with open(path + ".json", "w") as json_file:

                # In content, we add the data we retrieve.
                content = []
                for page_number in range(0, 1000) :
            
                    sleep(0.6) # Please dont sleep less than 0.5 for the server limit

                    response = requests.get(f'{self.base_url}/{path}?page[number]={page_number}', headers = {"Authorization": f"Bearer {self.public_token}"})

                    if response.status_code >= 400 :
                        print(response._content)
                        rm_f(path + ".json")
                        return print("something went wrong...")

                    tmp = eval(str(response.json()))
                    if tmp == []:
                        break

                    content.extend(tmp)

                json.dump(content, json_file, indent=4)

        #                _        _      _           _ 
        #  _ __ ___  ___| |_ _ __(_) ___| |_ ___  __| |
        # | '__/ _ \/ __| __| '__| |/ __| __/ _ \/ _` |
        # | | |  __/\__ \ |_| |  | | (__| ||  __/ (_| |
        # |_|  \___||___/\__|_|  |_|\___|\__\___|\__,_|
        #                                              

        def get_access_token(self):
            print("https://api.intra.42.fr/oauth/authorize?client_id=4c8b6090c10edd4d18bfe036d2ddaacffd63beb223edecdb761d7ebcf0ed7edd&redirect_uri=http%3A%2F%2Fgoogle.com&response_type=code&scope=public%20projects&state=a_very_long_random_string_witchmust_be_unguessable") # no state for now.
            if not self.code:
                self.code = input("Paste the code from the url: ")
            post_data = {
                'grant_type' : "authorization_code",
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'code' : self.code,
                'redirect_uri' : "http://google.com"
            }
            r = requests.post(self.access_token_url, data=post_data)
            response = r.json()
            self.access_token = response["access_token"]

        def get_json_restricted(self, path):

            if not self.access_token:
                self.get_access_token()

            mkdir_p('/'.join(path.split('/')[:-1]))
            rm_f(path + ".json")

            with open(path + ".json", "w") as json_file:

                # In content, we add the data we retrieve.
                content = []
                for page_number in range(0, 1000) :
            
                    sleep(1) # Please dont sleep less than 0.5 for the server limit, I use 1 so we can have more than one user at the time. + it shouldnt be more than 2 pages anyway

                    response = requests.get(f'{self.base_url}/{path}?page[number]={page_number}', headers = {"Authorization": f"Bearer {self.access_token}"})

                    if response.status_code >= 400 :
                        print(response.reason)
                        rm_f(path + ".json")
                        return print("something went wrong...")

                    tmp = eval(str(response.json()))
                    if tmp == []:
                        break

                    content.extend(tmp)

                json.dump(content, json_file, indent=4)

        #                 _                  
        #   ___ _   _ ___| |_ ___  _ __ ___  
        #  / __| | | / __| __/ _ \| '_ ` _ \ 
        # | (__| |_| \__ \ || (_) | | | | | |
        #  \___|\__,_|___/\__\___/|_| |_| |_|
        #                                   

        # I find the slots but still can't book them.
        def find_slots(self, project_id):
            import vlc
            import random

            print("\033[33mBe aware that this script will not work well the first 5 minutes, it needs to build up some data first.\033[m")

            if not self.access_token:
                self.get_access_token()

            discovered_slots = set()
            while (1):

                self.get_json_restricted(f"projects/{project_id}/slots")

                # protection against file deletion that might be caused by server overload
                if not os.path.isfile(f"projects/{project_id}/slots.json"):
                    continue

                with open(f"projects/{project_id}/slots.json") as json_slots :
                    data = json.load(json_slots)
                    newly_discovered_slots = set()
                    for slot in data:
                        slot_id = slot["id"]
                        if slot_id in discovered_slots:
                            continue

                        date = datetime.datetime.strptime(slot["begin_at"], '%Y-%m-%dT%H:%M:%S.000Z')
                        # I think that when slots are created, their id is greater than the previous slots.
                        if date.day == date.today().day and all(slot_id > ds for ds in discovered_slots):
                            p = vlc.MediaPlayer("notif.mp3")
                            p.play()
                            newly_discovered_slots.add(slot_id)
                            print(f"New slot for today {date.ctime()} discovered at {date.today().hour}h{date.today().minute}")

                    discovered_slots.update(newly_discovered_slots)

                # sleep is random for multi users
                sleep (random.randint(20, 30))
