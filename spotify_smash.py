import requests
import datetime
from heapq import heappop, heappush

# Get the top "song_count" songs from every user passed in
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "song_data")
def get_users_top_songs(user_tokens: list = [], song_count: int = 100) -> dict:
    song_dict = {}
    for token in user_tokens:
        # Make request for user's top songs
        response = requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit={min(song_count,50)}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        if response.status_code != 200:
            print(f"Failed to user top songs: {response.json()}")
            return {}

        song_obj = response.json()
        # Parse request to get song data
        item_list = song_obj['items']
        for single_song in item_list:
            song_id = single_song["id"]
            if song_id in song_dict:
                song_dict[song_id]["total_users"] += 1
            else: 
                song_dict[song_id] = {
                    "total_users": 1,
                    "song_data": single_song
                }
    return song_dict

# Get audio features for each song in the dictionary
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "song_data", "audio_features")
def get_audio_features(user_tokens: list = [], song_dict: dict = {}) -> dict:
    song_features = song_dict
    for song_id in song_dict:
        response = requests.get(
            f"https://api.spotify.com/v1/audio-features/{song_id}",
            headers={
                "Authorization": f"Bearer {user_tokens[0]}"
            }
        )
        song_response = response.json()
        song_features[song_id]["audio_features"] = song_response
    return song_features

# Rank songs by certain features
# Returns a max-heap for each category by score
# Each heap is indexed in a dict by category name
def rank_songs(songs_features: dict = {}, rank_categories: list = []) -> dict:
    category_heap = {}
    for song_id in songs_features:
        for category in rank_categories:
            category_score = songs_features[song_id]["audio_features"][category]
            category_tuple = (-category_score, song_id)
            if category in category_heap:
                heappush(category_heap[category], category_tuple)
            else:
                category_heap[category] = []
                heappush(category_heap[category], category_tuple)
    return category_heap

'''
token = ""
rank_categories = ["danceability", "energy", "acousticness"]
top_songs = get_users_top_songs([token], 5)
audio_features = get_audio_features([token], top_songs)
heap = rank_songs(audio_features, rank_categories)
print(heap)
'''

# Gets top songs from each category
# Returns a list of songIDs for the final playlist
def get_top_category_songs(ranked_songs: dict = {}, total_songs: int = 100) -> list:
    pass


# Make the final spotify playlist from the songs
# Returns identifier of the new playlist
def make_final_playlist(user_tokens: list = [], final_songs: list = [], user_id: str = "") -> str:
    playlist = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers={
            "Authorization": f"Bearer {user_tokens[0]}"
        },
        data = {
            "name": f"Spotify Smash {datetime.datetime.now().isoformat()}",
            "description": "A SUPER SMASHIN PLAYLIST",
            "public": True,
            "collaborative": True
        }
    )
    playlist_id = playlist.json()["id"]

    add_songs = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": f"Bearer {user_tokens[0]}"
        },
        data = {
            "uris": final_songs
        }
    )
    return playlist_id


# Add playlist to each user's account
def add_playlist_to_accounts(user_tokens: list = [], playlist_id: str = '') -> None:
    for i in range(1, len(user_tokens)):
        add_playlists = requests.put(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/followers",
            headers={
                "Authorization": f"Bearer {user_tokens[i]}"
            }
        )


# Entry code and argument handling
if __name__ == "__main__":
    pass