from typing import List
import requests

from take3breaths_scrapper.schema import Tag, Track, TrackTagAssociation
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

tags: List[Tag] = []
associations: List[TrackTagAssociation] = []

for track in tracks:
    for tag_name in track.tags:
        tag = next((t for t in tags if t.name == tag_name), None)
        if tag is None:
            tag = Tag(name=tag_name)
            tags.append(tag)
        associations.append(
            TrackTagAssociation(track_name=track.name, tag_name=tag.name)
        )


save_insert_statements_to_file(tracks, "tracks", "tracks.sql")
save_insert_statements_to_file(tags, "tags", "tags.sql")
save_insert_statements_to_file(associations, "associations", "associations.sql")
