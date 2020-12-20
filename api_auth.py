import json, os, requests
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
            self.grant_type = "client_credentials"
            self.authorize_url = "https://api.intra.42.fr/oauth/authorize"
            self.access_token_url = "https://api.intra.42.fr/oauth/token"
            self.base_url = "https://api.intra.42.fr/v2"
            self.access_token = None
            self.code = None


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


        def get_json(self, path):
            
            mkdir_p('/'.join(path.split('/')[:-1]))
            rm_f(path + ".json")

            with open(path + ".json", "a") as json_file:

                # In content, we add the data we retrieve.
                content = []
                for page_number in range(0, 200) :
            
                    sleep(0.6) # Please dont sleep less than 0.5 for the server limit

                    response = requests.get(f'{self.base_url}/{path}?page[number]={page_number}&filer=5', headers = {"Authorization": f"Bearer {self.access_token}"})

                    # Print the status once in a while
                    if page_number % 10 == 0:
                        print("Status code:", response.status_code)
                        if response.status_code >= 400 :
                            print(response.text)
                            return print("something went wrong...")

                    tmp = eval(str(response.json()))
                    if tmp == []:
                        break

                    content.extend(tmp)

                json.dump(content, json_file, indent=4)


connection = OAuth42()
connection.get_access_token()

print("\033[33mRetrieve my teams\033[m")
connection.get_json("me/teams")
print("\033[33mFind slots\033[m")
connection.get_json("projects/1342/slots")

# Trying to take a slot
# connection.get_json("slots/{slot_id}")