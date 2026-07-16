from src.recommender.spotify_client import search_tracks

songs = search_tracks("calm")

print("\nRecommended Songs:\n")

for i, song in enumerate(songs, start=1):
    print(f"{i}. {song['song']} - {song['artist']}")
    print(song["url"])
    print("-" * 50)