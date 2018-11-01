import requests
import time

# _


with open("team_ids_6", "w") as team_id_file:

    for x in range(1830, 1840):
        try:
            tmp = requests.get("https://api.kivaws.org/v1/teams/search.json?page=%s" % str(x))
            if tmp.status_code == 200:
                myTeams = tmp.json()["teams"]
                print(x)
                for team in myTeams:
                    team_id_file.write(str(team["id"]) + "\n")
            else:
                print("Page #%s retrieval failed with code %s" %(x, tmp.status_code))
                print(tmp.text)
            
            time.sleep(1)

        except:
            print("Could not retrieve page # ", x)
            time.sleep(1)