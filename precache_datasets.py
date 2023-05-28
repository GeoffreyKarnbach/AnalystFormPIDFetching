import json
import os

def convert_dataset_link_to_file(pid_link):

    response = os.popen(f'curl -LH "Accept: application/json" -k {pid_link}').read()
    with open(f"datasets_metadata/{pid_link.split('/')[-1]}.json","w") as f:
        f.write(response)

def main():
    content = json.load(open("datasets_metadata/datasets.json"))

    for dataset in content:
        convert_dataset_link_to_file(dataset['main'])
        for subset in dataset["subsets"]:
            convert_dataset_link_to_file(subset)


if __name__ == "__main__":
    main()