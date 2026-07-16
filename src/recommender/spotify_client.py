import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Load .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
)

def search_tracks(query, limit=10):

    results = sp.search(
        q=query,
        type="track",
        limit=limit
    )

    songs = []

    for track in results["tracks"]["items"]:

        songs.append({
            "song": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"]
        })

    return songs