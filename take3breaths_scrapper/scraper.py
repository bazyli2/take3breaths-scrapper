import requests

from take3breaths_scrapper.schema import Track
from take3breaths_scrapper.utils import save_objects_to_csv

response = requests.post(
    "https://api.dev.mindses.com/v1/login/",
    data={"email": "testowaosoba122+51@gmail.com", "password": "jeremi420"},
)
json = response.json()
response = requests.get(
    "https://api.dev.mindses.com/v1/tracks/",
    headers={"Authorization": "Bearer " + json["access_token"]},
)
json = response.json()
tracks = list(map(Track.model_validate, json))
for track in tracks:
    track.download_image()
    track.download_audio()
    track.download_sample()

save_objects_to_csv(tracks, "tracks.csv")
