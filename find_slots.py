from OAuth42 import OAuth42
from time import sleep
import vlc, random, json, datetime, os

connection = OAuth42()

def find_slots(project_id):

    print("\033[33mBe aware that this script will not work well the first 5 minutes, it needs to build up some data first.\033[m")

    if not connection.access_token:
        connection.get_access_token()

    discovered_slots = set()

    while (1):

        connection.get_json_restricted(f"projects/{project_id}/slots")
        
        # protection against file deletion that might be caused by server overload
        if not os.path.isfile(f"projects/{project_id}/slots.json"):
            continue
        
        print('.', end='', flush=True) # to show progress
        
        with open(f"projects/{project_id}/slots.json") as json_slots :
        
            data = json.load(json_slots)
            newly_discovered_slots = set()
        
            for slot in data:
        
                slot_id = slot["id"]
        
                if slot_id in discovered_slots:
                    continue
        
                date = datetime.datetime.strptime(slot["begin_at"], '%Y-%m-%dT%H:%M:%S.000Z')
        
                # I think that when slots are created, their id is greater than the previous slots.
                if date.day in [date.today().day, date.today().day + 1] and all(slot_id > ds for ds in discovered_slots) and (date - datetime.datetime.now()).total_seconds() / 3600 > 0.5:
                    p = vlc.MediaPlayer("notif.mp3")
                    p.play()
                    newly_discovered_slots.add(slot_id)
                    print(f"\033[36m\rNew slot for {date.ctime()} discovered at {date.today().hour}h{date.today().minute:02}\033[m")
        
            discovered_slots.update(newly_discovered_slots)

        # sleep is random for multi users
        sleep (random.randint(30, 40))


# print("\033[33mRetrieve my teams\033[m")
# connection.get_json_restricted("me/teams")

print("\033[33mFind slots\033[m")
project_id = 1348 # CPP-04_id = 1348
find_slots(project_id)
