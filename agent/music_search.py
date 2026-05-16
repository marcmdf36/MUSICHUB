import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from agent.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

_client = None

# Diccionario de queries por género.
# Para añadir/quitar géneros, edita aquí y en config.py
SEARCH_QUERIES = {
    "rock": [
        "genre:rock", "genre:alternative", "genre:garage rock",
        "genre:post-punk", "genre:psych rock",
    ],
    "indie": [
        "genre:indie", "genre:indie pop", "genre:indie rock",
        "genre:dream pop", "genre:shoegaze",
    ],
    "electronic": [
        "genre:electronic", "genre:ambient", "genre:idm",
        "genre:downtempo", "genre:electronica",
    ],
    "house": [
        "genre:house", "genre:deep house", "genre:progressive house",
        "genre:disco house", "genre:uk garage",
    ],
    "techno": [
        "genre:techno", "genre:minimal techno", "genre:detroit techno",
        "genre:dub techno", "genre:acid techno",
    ],
    "classical": [
        "genre:classical", "genre:orchestra", "genre:piano classical",
        "genre:contemporary classical", "genre:baroque",
    ],
    "jazz": [
        "genre:jazz", "genre:bebop", "genre:cool jazz",
        "genre:jazz fusion", "genre:modal jazz",
    ],
    "hiphop": [
        "genre:hip hop", "genre:rap", "genre:boom bap",
        "genre:conscious hip hop", "genre:underground hip hop",
    ],
    "soul": [
        "genre:soul", "genre:neo soul", "genre:funk",
        "genre:motown", "genre:r&b",
    ],
}


def _get_client() -> spotipy.Spotify:
    global _client
    if _client is None:
        auth = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )
        _client = spotipy.Spotify(auth_manager=auth)
    return _client


def _search_tracks(query: str, limit: int = 10, offset: int = 0) -> list[dict]:
    """Busca canciones en Spotify y devuelve datos estructurados."""
    sp = _get_client()
    try:
        results = sp.search(q=query, type="track", limit=limit, offset=offset)
    except Exception:
        return []

    tracks = []
    for track in results.get("tracks", {}).get("items", []):
        try:
            tracks.append({
                "title": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "year": track["album"]["release_date"][:4] if track["album"].get("release_date") else None,
                "spotify_url": track["external_urls"]["spotify"],
                "album_cover": track["album"]["images"][0]["url"] if track["album"].get("images") else None,
                "popularity": track.get("popularity", 0),
            })
        except (KeyError, IndexError):
            continue
    return tracks


def fetch_candidates(genres: list[str], per_genre: int = 10) -> list[dict]:
    """Genera un pool de candidatas reales buscando en Spotify por género."""
    candidates = []
    seen = set()  # Evitar duplicados por título+artista

    for genre in genres:
        queries = SEARCH_QUERIES.get(genre, [f"genre:{genre}"])
        # Elegir queries aleatorias para variedad entre ejecuciones
        selected_queries = random.sample(queries, min(2, len(queries)))

        for query in selected_queries:
            # Offset aleatorio para no obtener siempre los mismos resultados
            offset = random.randint(0, 200)
            tracks = _search_tracks(query, limit=per_genre, offset=offset)

            for track in tracks:
                key = (track["title"].lower(), track["artist"].lower())
                if key not in seen:
                    track["genre"] = genre
                    candidates.append(track)
                    seen.add(key)

    random.shuffle(candidates)
    return candidates


def format_candidates_for_llm(candidates: list[dict]) -> str:
    """Formatea el pool como texto para el prompt."""
    lines = []
    for i, song in enumerate(candidates, 1):
        lines.append(
            f"{i}. {song['artist']} - {song['title']} "
            f"({song['genre']}, {song['year']}, popularidad: {song['popularity']})"
        )
    return "\n".join(lines)


def get_candidate_by_index(candidates: list[dict], title: str, artist: str) -> dict | None:
    """Busca una canción en el pool por título y artista."""
    for c in candidates:
        if c["title"].lower() == title.lower() and c["artist"].lower() == artist.lower():
            return c
    return None