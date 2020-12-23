from OAuth42 import OAuth42
from time import sleep
import vlc, random, json, datetime, os

#        _   _ _     
#  _   _| |_(_) |___ 
# | | | | __| | / __|
# | |_| | |_| | \__ \
#  \__,_|\__|_|_|___/
#                    

def show_progress():
    print('.', end='', flush=True)

def print_warning(str):
    print(f"\033[33m{str}\033[m")

def sound_notif():
    p = vlc.MediaPlayer("notif.mp3")
    p.play()

def show_new_slot(date):
    print(f"\033[36m\rNew slot for {date.ctime()} discovered at {date.today().hour}h{date.today().minute:02}\033[m")

def date_time_42format(date42):
    return datetime.datetime.strptime(date42, '%Y-%m-%dT%H:%M:%S.000Z')

#                  _       
#  _ __ ___   __ _(_)_ __  
# | '_ ` _ \ / _` | | '_ \ 
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
#                          

if __name__ == "__main__":
    
    connection = OAuth42()
    connection.get_access_token()

    # print("\033[33mRetrieve my teams\033[m") # test connection, chek the projects_ids, ...
    # connection.get_json_restricted("me/teams")

    project_id = 1348 # CPP-04_id

    print_warning("find_slot: Be aware that this script will not work well the first 5 minutes, it needs to build up some data first.")

    discovered_slots = set()

    while (1):

        show_progress()

        connection.get_json_restricted(f"projects/{project_id}/slots", max_nb_page=20)

        with open(f"projects/{project_id}/slots.json") as json_slots :        

            newly_discovered_slots = set()

            for slot in json.load(json_slots):
            
                slot_id = slot["id"]

                if slot_id in discovered_slots:
                    continue
                
                date = date_time_42format(slot["begin_at"])

                if date.day in [date.today().day, date.today().day + 1] and all(slot_id > ds for ds in discovered_slots) and (date - datetime.datetime.now()).total_seconds() / 3600 > 0.5:
                    sound_notif()
                    newly_discovered_slots.add(slot_id)
                    show_new_slot(date)

            discovered_slots.update(newly_discovered_slots)

        sleep (random.randint(50, 60)) # sleep is random for multi users
