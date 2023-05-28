import requests
import json
import os

#base_url = "http://localhost:9096"
base_url = "https://dbrepo1.ec.tuwien.ac.at"

identifier_endpoint = "/api/identifier"

# Get all identifiers
response = requests.get(base_url + identifier_endpoint)
identifiers = response.json()

temp_datasets = {}
database_id_to_pid = {}

# Get all identifiers of type "database"
for identifier in identifiers:
    if identifier["type"] == "database":
        temp_datasets[identifier["database_id"]] = []
        database_id_to_pid[identifier["database_id"]] = identifier["id"]

# Get all identifiers of type "subset" and add to parent database
for identifier in identifiers:
    if identifier["type"] == "subset":
        temp_datasets[identifier["database_id"]].append(identifier["id"])



# Replace database_id with pid
datasets= []
for database_id in temp_datasets.keys():
    datasets.append({})
    datasets[-1]["main"] = base_url + "/pid/" + str(database_id_to_pid[database_id])
    datasets[-1]["subsets"] = []
    for subset_id in temp_datasets[database_id]:
        datasets[-1]["subsets"].append(base_url + "/pid/" + str(subset_id))

os.makedirs("datasets_metadata", exist_ok=True)

with open('datasets_metadata/datasets.json', 'w') as outfile:
    json.dump(datasets, outfile, indent=4)

