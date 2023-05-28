import yaml
from yaml.loader import SafeLoader

filename = input("Enter the name of the docker-compose.yml file: ")

# Load the docker-compose.yml file
with open(filename, "r") as f:
    data = yaml.load(f, Loader=SafeLoader)


# Get the services and their dependencies
services = {}

for service in data["services"]:
    services[service] = []
    if "depends_on" in data["services"][service]:
        for dependency in data["services"][service]["depends_on"]:
            services[service].append(dependency)

# Change service->dependencies to dependencies->service
servicesDependencies = {}

for service in services:
    for dependency in services[service]:
        if dependency not in servicesDependencies:
            servicesDependencies[dependency] = []
        servicesDependencies[dependency].append(service)

# Make adjacency matrix
adjacencyMatrix = [[0 for i in range(len(services))] for j in range(len(services))]

for service in services:
    for dependency in services[service]:
        adjacencyMatrix[list(services.keys()).index(service)][list(services.keys()).index(dependency)] = 1

# Print out table in machine readable format for
# https://csacademy.com/app/graph_editor/
for service in servicesDependencies:
    print(service)

for service in servicesDependencies:
    for dependency in servicesDependencies[service]:
        print(service, dependency)

print("\n\n")

# Print out table in human readable format
print("Services depending on:")
for service in servicesDependencies:
    print(service, ":")
    for dependency in servicesDependencies[service]:
        print("\t", dependency)
