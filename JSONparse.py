import json
import csv

# with open('Data/team_data/teamdata_0_99') as f:
#     data = json.load(f)


with open("teamdata_processed.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    import glob

    path = "Data/team_data/*.json"
    for x in glob.glob(path):
        print x
        with open(x) as f:
            data = json.load(f)
            for indexi, vali in enumerate(data):
                for indexj, valj in enumerate(data[indexi]["lenders"]):
                    try:
                        if not data[indexi]["lenders"][indexj]["name"] == 'Anonymous':
                            print indexi, indexj
                            writer.writerow((data[indexi]["team_id"], data[indexi]["lenders"][indexj]["uid"]))
                        else:
                            continue
                    except:
                        continue

