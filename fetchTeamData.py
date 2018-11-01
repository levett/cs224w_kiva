import requests
import time
import json

NUM_TEAMS = 36128
lastTeamCount = 0
teamCount = 0

# Save team data in a file for every 100 teams.
increment = 100
lines = []

# Read the team id file.
with open("Data/team_data/team_ids", "r") as team_id_file:
    lines = [line.rstrip('\n') for line in team_id_file]

myJSON = []

# Fetch the team data.
while teamCount < NUM_TEAMS:
    try:
        team_id = int(lines[teamCount])
        print("count %s, id %s" % (teamCount, team_id))
        tmp = requests.get("https://api.kivaws.org/v1/teams/%s/lenders.json" % str(team_id))
        if tmp.status_code == 200:
            tmpJSON = tmp.json()
            # Add team id since that's not super obvious.
            tmpJSON["team_id"] = team_id
            myJSON.append(tmpJSON)
        else:
            print("Team #%s data retrieval failed with code %s" %(x, tmp.status_code))
            print(tmp.text)
        
        time.sleep(1)

    except:
        print("Could not retrieve team # ", x)
        time.sleep(1)

    teamCount += 1

    # Print data to file for every 100 teams.
    if teamCount == lastTeamCount + increment:
        filename = "Data/team_data/teamdata_" + str(lastTeamCount) + "_" + str(teamCount - 1)
        with open(filename, "w") as team_data_file:
            team_data_file.write(json.dumps(myJSON, separators=(',',':')))
            print("data printed to %s" % filename)
        lastTeamCount = teamCount
        myJSON = []

# Print the rest of the data to file.
if lastTeamCount != teamCount:
    filename = "Data/team_data/teamdata_" + str(lastTeamCount) + "_" + str(teamCount - 1)
    with open(filename, "w") as team_data_file:
        team_data_file.write(json.dumps(myJSON, separators=(',',':')))
        print("data printed to %s" % filename)
