from feast import FeatureStore
import pandas as pd
import requests
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-e",
    "--entities",
    default="100,101",
    help="Trip ids to fetch prediction for. Comma separated list of trip ids",
)

args = parser.parse_args()

parsed_args = vars(args)
entities = parsed_args["entities"].split(",")

entity_dicts = []

for entity in entities:
    entity_dicts.append({"trip_id": int(entity)})

store = FeatureStore(repo_path="feature_repo/")

features = store.get_online_features(
    features=[
        "trip_details_online_stream:dropoff_latitude",
        "trip_details_online_stream:Distance",
        "trip_details_online_stream:Monthly_Quarter_Q4",
        "trip_details_online_stream:Hourly_Segments_H3",
        "trip_details_online_stream:Hourly_Segments_H4",
        "trip_details_online_stream:Hourly_Segments_H5",
        "trip_details_online_stream:year_2012",
        "trip_details_online_stream:year_2013",
        "trip_details_online_stream:year_2014",
        "trip_details_online_stream:year_2015",
    ],
    entity_rows=entity_dicts,
).to_dict(include_event_timestamps=False)

def print_online_features(features):
    for key, value in sorted(features.items()):
        print(key, " : ", value)

print_online_features(features)

print()

val = pd.DataFrame().from_dict(features).drop("trip_id", axis=1)

for i in range(len(val)):
    predict_dict = {"features": val.iloc[i].values.tolist()}

    headers = {"Content-Type": "application/json"}

    resp = requests.post("http://localhost:5001/predict", headers=headers, data=json.dumps(predict_dict))

    predictions = json.loads(resp.content.decode('utf-8'))

    if "predictions" in predictions.keys():
        print("Fare Prediction for trip id " + entities[i] + " is: " + str(predictions["predictions"][0]))
    else:
        print("None values retrieved for the given trip id: " + entities[i])