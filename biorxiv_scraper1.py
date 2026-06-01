

import requests
import csv
import json
import requests
import time

def save_to_csv(data, filename="unpublished_neuroscience_preprints.csv"):
    """Saves the collected data into a structured CSV file."""
    if not data:
        print("No data available to save.")
        return   
    keys = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved {len(data)} rows to {filename}")

base = "https://api.biorxiv.org/details/biorxiv/2017-01-01/2024-01-01"
cursor = 0
all_preprints = []
unpublished_neuro_preprints = []
while True:
    resp = requests.get(f"{base}/{cursor}").json()
    records = resp.get("collection", [])
    # print(records)
    # stop
    if not records:
        break
    for paper in records:
        # Check if the category is Neuroscience and if it lacks a published journal DOI
        if paper.get('category') == 'neuroscience' and paper.get('published')=='NA':
            print('found one!')
            print([paper])
            unpublished_neuro_preprints.append({
                'title': paper.get('title'),
                'author_corresponding': paper.get('author_corresponding'),
                'doi': paper.get('doi'),
                'authors': paper.get('authors'),
                'date': paper.get('date')
            })
            save_to_csv(unpublished_neuro_preprints)
    cursor += 30
    all_preprints.extend(records)
    print(f"Total preprints retrieved: {len(all_preprints)}")
    # if cursor>3000:
print(unpublished_neuro_preprints)
        # break