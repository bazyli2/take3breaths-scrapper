import requests

from take3breaths_scrapper.schema import Track
from take3breaths_scrapper.utils import (
    save_insert_statements_to_file,
)

response = requests.post(
    "https://api.dev.mindses.com/v1/login/",
    data={"email": "lifaleca@jollyfree.com", "password": "jeremi421"},
)
json = response.json()
response = requests.get(
    "https://api.dev.mindses.com/v1/tracks/",
    headers={"Authorization": "Bearer " + json["access_token"]},
)
json = response.json()
tracks = list(map(Track.model_validate, json))
# for track in tracks:
#     track.download_image()
#     track.download_audio()
#     track.download_sample()

save_insert_statements_to_file(tracks, "tracks.sql")
