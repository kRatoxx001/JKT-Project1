from backend.app.core.config import get_settings


EMOTION_AUDIO_PROFILES = {
    "joy": {"seed_genres": ["pop"], "target_valence": 0.86, "target_energy": 0.78},
    "sadness": {"seed_genres": ["acoustic"], "target_valence": 0.32, "target_energy": 0.35},
    "anger": {"seed_genres": ["rock"], "target_valence": 0.46, "target_energy": 0.88},
    "fear": {"seed_genres": ["ambient"], "target_valence": 0.42, "target_energy": 0.28},
    "love": {"seed_genres": ["r-n-b"], "target_valence": 0.74, "target_energy": 0.48},
    "surprise": {"seed_genres": ["dance"], "target_valence": 0.8, "target_energy": 0.82},
    "neutral": {"seed_genres": ["chill"], "target_valence": 0.58, "target_energy": 0.5},
}

FALLBACK_TRACKS = {
    "joy": [
        ("Golden Hour Drive", "NOVA Lane", "happy pop", 94),
        ("Skyline Lift", "The North Signal", "dance pop", 89),
        ("Good News Static", "Mira Vale", "indie pop", 84),
    ],
    "sadness": [
        ("Late Bloom", "Aster Theory", "acoustic", 91),
        ("Window Weather", "Mira Vale", "soft indie", 86),
        ("Quiet Return", "NOVA Lane", "piano calm", 81),
    ],
    "anger": [
        ("Static Run", "The North Signal", "alt rock", 92),
        ("Redline Reset", "Aster Theory", "rock", 88),
        ("Fuse Break", "NOVA Lane", "workout rock", 83),
    ],
    "fear": [
        ("Steady Lights", "Mira Vale", "calm", 93),
        ("Soft Landing", "Aster Theory", "ambient pop", 87),
        ("Small Horizon", "NOVA Lane", "chill", 82),
    ],
    "love": [
        ("Soft Static", "Mira Vale", "romantic", 93),
        ("Close Enough", "Aster Theory", "r&b", 87),
        ("Bloom Signal", "The North Signal", "warm pop", 82),
    ],
    "surprise": [
        ("Bright Detour", "NOVA Lane", "party", 91),
        ("Turn the Corner", "The North Signal", "funk pop", 86),
        ("Lift Off", "Aster Theory", "electropop", 82),
    ],
    "neutral": [
        ("Middle Distance", "Mira Vale", "chill pop", 86),
        ("Clean Slate", "NOVA Lane", "focus", 82),
        ("Low Sun", "Aster Theory", "indie", 78),
    ],
}


def build_playlist(emotion: str, confidence: float) -> dict:
    normalized = emotion.lower()
    profile = EMOTION_AUDIO_PROFILES.get(normalized, EMOTION_AUDIO_PROFILES["neutral"])
    spotify_tracks = _get_spotify_recommendations(profile)

    tracks = spotify_tracks or [
        {"title": title, "artist": artist, "mood": mood, "match": match, "spotify_uri": None}
        for title, artist, mood, match in FALLBACK_TRACKS.get(normalized, FALLBACK_TRACKS["neutral"])
    ]

    return {
        "playlist_name": f"{normalized.title()} Reset Mix",
        "summary": _summary_for(normalized),
        "confidence": confidence,
        "tracks": tracks,
        "spotify_enabled": bool(spotify_tracks),
        "spotify_profile": profile,
    }


def get_spotify_auth_url() -> str:
    auth_manager = _get_user_auth_manager()
    return auth_manager.get_authorize_url()


def handle_spotify_callback(code: str) -> dict:
    auth_manager = _get_user_auth_manager()
    token_info = auth_manager.get_access_token(code, as_dict=True)
    return {
        "access_token": bool(token_info.get("access_token")),
        "scope": token_info.get("scope"),
        "expires_at": token_info.get("expires_at"),
    }


def save_playlist_to_spotify(name: str, description: str, track_uris: list[str]) -> dict:
    auth_manager = _get_user_auth_manager()

    try:
        import spotipy

        spotify = spotipy.Spotify(auth_manager=auth_manager)
        user = spotify.current_user()
        playlist = spotify.user_playlist_create(
            user=user["id"],
            name=name,
            public=False,
            description=description,
        )
        if track_uris:
            spotify.playlist_add_items(playlist["id"], track_uris)
    except Exception as exc:
        raise RuntimeError("Spotify playlist creation failed") from exc

    return {
        "playlist_id": playlist["id"],
        "external_url": playlist.get("external_urls", {}).get("spotify"),
    }


def _get_spotify_recommendations(profile: dict) -> list[dict]:
    settings = get_settings()
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        return []

    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials

        auth_manager = SpotifyClientCredentials(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
        )
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        response = spotify.recommendations(limit=8, **profile)
    except Exception:
        return []

    tracks = []
    for item in response.get("tracks", []):
        artists = ", ".join(artist["name"] for artist in item.get("artists", []))
        tracks.append(
            {
                "title": item.get("name", "Untitled"),
                "artist": artists or "Unknown artist",
                "mood": profile["seed_genres"][0],
                "match": 90,
                "spotify_uri": item.get("uri"),
                "preview_url": item.get("preview_url"),
                "external_url": item.get("external_urls", {}).get("spotify"),
            }
        )

    return tracks


def _get_user_auth_manager():
    settings = get_settings()
    if not settings.spotify_client_id or not settings.spotify_client_secret:
        raise RuntimeError("Spotify credentials are not configured")

    from spotipy.oauth2 import SpotifyOAuth

    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=settings.spotify_redirect_uri,
        scope="user-read-private playlist-modify-private playlist-modify-public",
        cache_path=".spotify_cache",
        show_dialog=True,
    )


def _summary_for(emotion: str) -> str:
    summaries = {
        "joy": "Upbeat, bright tracks with high valence and enough momentum to keep the good mood moving.",
        "sadness": "Soft acoustic and warm low-tempo tracks for comfort without making the room heavier.",
        "anger": "High-energy rock and focused beats to let pressure move without losing control.",
        "fear": "Calm, grounded tracks with lower tempo and smoother textures to help regulate the moment.",
        "love": "Warm romantic tracks with gentle rhythm and intimate vocals.",
        "surprise": "Playful, varied tracks with a little bounce and unexpected movement.",
        "neutral": "Balanced recommendations that can work while studying, commuting, or resetting.",
    }
    return summaries.get(emotion, summaries["neutral"])
