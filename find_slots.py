from OAuth42 import OAuth42

connection = OAuth42()

# print("\033[33mRetrieve my teams\033[m")
# connection.get_json_restricted("me/teams")

print("\033[33mFind slots\033[m")
project_id = 1348 # CPP-04_id = 1348
connection.find_slots(project_id)
