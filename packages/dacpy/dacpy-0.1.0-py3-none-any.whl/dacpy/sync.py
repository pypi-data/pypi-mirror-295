import re
from typing import List, Tuple, Dict, Optional
from urllib.parse import urlparse

import hishel
import httpx
import spotipy
import platformdirs
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from fuzzywuzzy import fuzz

from dacpy.settings import Settings

s = Settings()


def get_spotify() -> spotipy.Spotify:
    scope = "user-library-read playlist-modify-public playlist-modify-private"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=s.spotify_client_id,
        client_secret=s.spotify_client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope=scope,
        cache_handler=CacheFileHandler(cache_path=platformdirs.user_cache_path("dacpy") / "spotipy.cache")
    ))


def get_lb() -> httpx.Client:
    return hishel.CacheClient(
        headers={"Authorization": f"Token {s.listenbrainz_token}"},
        base_url="https://api.listenbrainz.org/",
        storage=hishel.FileStorage(base_path=platformdirs.user_cache_path("dacpy"))
    )


def extract_uuid_from_url(url: str) -> Optional[str]:
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'
        match = re.search(uuid_pattern, path)
        return match.group(1) if match else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_lb_username(lb: httpx.Client) -> str:
    response = lb.get("1/validate-token")
    if response.status_code == 200:
        data = response.json()
        return data["user_name"]
    return ""


def get_lb_playlist_by_name(lb: httpx.Client, name: str) -> Optional[Dict]:
    username = get_lb_username(lb)
    response = lb.get(f"/1/user/{username}/playlists", params={"name": name})
    if response.status_code == 200:
        playlists = response.json()
        for playlist in playlists["playlists"]:
            if playlist["playlist"]["title"] == name:
                mbid = extract_uuid_from_url(playlist["playlist"]["identifier"])
                response = lb.get(f"1/playlist/{mbid}")
                if response.status_code == 200:
                    return response.json()
    return None


def get_sp_playlist_by_name(sp: spotipy.Spotify, name: str) -> Optional[Dict]:
    playlists = sp.current_user_playlists()
    for playlist in playlists["items"]:
        if playlist["name"] == name:
            return playlist
    return None


def clean_track_name(track_name: str) -> str:
    cleaned_name = re.sub(r'\([^)]*\)', '', track_name)
    cleaned_name = re.sub(r'\[[^]]*]', '', cleaned_name)
    keywords_to_remove = ['remix', 'feat', 'ft', 'featuring', 'edit', 'version', "part"]
    for keyword in keywords_to_remove:
        cleaned_name = re.sub(rf'\b{keyword}\b', '', cleaned_name, flags=re.IGNORECASE)
    return ' '.join(cleaned_name.split()).strip()


def parse_artist_name(artist_name: str) -> Tuple[str, List[str]]:
    featured_split = re.split(r'\s+(?:feat\.?|ft\.?|featuring)\s+', artist_name, flags=re.IGNORECASE)
    main_artist = featured_split[0].strip()
    featured_artists = [artist.strip() for artist in featured_split[1:]]
    main_artists = re.split(r'\s*[&,]\s*|\s+and\s+', main_artist)
    return main_artists[0], featured_artists + main_artists[1:]


def fuzzy_match_tracks(sp_tracks: List[Dict], lb_track: Tuple[str, List[str], str, int],
                       threshold: int = 60, duration_weight: float = 0.2) -> Optional[Dict]:
    best_match = None
    best_score = 0

    lb_track_name, lb_artists, lb_album_name, lb_duration_ms = lb_track

    for sp_track in sp_tracks:
        track_score = fuzz.ratio(sp_track["name"].lower(), lb_track_name.lower())

        artist_scores = [max(fuzz.ratio(sp_artist["name"].lower(), lb_artist.lower())
                             for sp_artist in sp_track["artists"])
                         for lb_artist in lb_artists]
        artist_score = sum(artist_scores) / len(artist_scores) if artist_scores else 0

        album_score = fuzz.ratio(sp_track["album"]["name"].lower(), lb_album_name.lower())

        duration_diff = abs(sp_track["duration_ms"] - lb_duration_ms)
        max_duration = max(sp_track["duration_ms"], lb_duration_ms)
        duration_score = 100 * (1 - duration_diff / max_duration)

        total_score = (
                (track_score + artist_score + album_score) * (1 - duration_weight) / 3 +
                duration_score * duration_weight
        )

        if total_score > best_score and total_score >= threshold:
            best_score = total_score
            best_match = sp_track

    return best_match


def fallback_search(sp: spotipy.Spotify, track_name: str) -> List[Dict]:
    query = f"track:{track_name}"
    return sp.search(q=query, type="track", limit=50)["tracks"]["items"]


def get_sp_ids(sp: spotipy.Spotify, track_names: List[Tuple[str, str, str, int]]) -> List[str]:
    sp_ids = []
    for track_name, artist_name, album_name, duration_ms in track_names:
        main_artist, featured_artists = parse_artist_name(artist_name)
        all_artists = [main_artist] + featured_artists

        query = f"track:{track_name} artist:{main_artist}"
        results = sp.search(q=query, type="track", limit=50)["tracks"]["items"]
        if not results:
            print(f"Track {track_name}, {artist_name} not found from original query:  `{query}`")
            # Try with cleaned track name
            cleaned_track_name = clean_track_name(track_name)
            query = f"track:{cleaned_track_name} artist:{main_artist}"
            results = sp.search(q=query, type="track", limit=50)["tracks"]["items"]

        if not results:
            print(f"Track {track_name}, {artist_name} not found from cleaned query:  `{query}`")
            # Try partial matching
            partial_name = ' '.join(track_name.split()[:3])
            query = f"track:{partial_name} artist:{main_artist}"
            results = sp.search(q=query, type="track", limit=50)["tracks"]["items"]

        if not results:
            print(f"Track {track_name}, {artist_name} not found from partial query:  `{query}`")
            # Fallback search with just the track name
            results = fallback_search(sp, track_name)

        best_match = fuzzy_match_tracks(results, (track_name, all_artists, album_name, duration_ms), threshold=45)

        if best_match:
            print(f"Adding track `{track_name},{album_name}` from query `{query}`")
            sp_ids.append(best_match["id"])
        else:
            print(f"Track {track_name}, {artist_name} not found from any query")
    print(f"found {len(sp_ids)}/{len(track_names)} tracks")
    return sp_ids


def empty_playlist(sp: spotipy.Spotify, playlist: Dict) -> None:
    tracks = sp.playlist_items(playlist["id"])
    offset = tracks["offset"]
    while len(tracks["items"]) > 0:
        sp.playlist_remove_all_occurrences_of_items(playlist["id"], [t["track"]["id"] for t in tracks["items"]])
        tracks = sp.playlist_items(playlist["id"], offset=offset)
        offset = tracks["offset"]


def main(playlist_name: str) -> str:
    sp = get_spotify()
    lb = get_lb()
    lb_playlist = get_lb_playlist_by_name(lb, playlist_name)
    sp_playlist = get_sp_playlist_by_name(sp, playlist_name)

    if not lb_playlist or not sp_playlist:
        raise ValueError("ListenBrainz or Spotify playlist not found")
    sp.playlist_change_details(sp_playlist["id"], description=lb_playlist["playlist"].get("annotation"))

    track_info = [(t["title"], t["creator"], t["album"], t.get("duration_ms", 0))
                  for t in lb_playlist["playlist"]["track"]]
    sp_ids = get_sp_ids(sp, track_info)

    empty_playlist(sp, sp_playlist)
    for i in range(0, len(sp_ids), 25):
        sp.playlist_add_items(sp_playlist["id"], sp_ids[i:i + 25])

    return sp_playlist["id"]
