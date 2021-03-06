import requests
import argparse
import datetime
from heapq import heappop, heappush
import sys
import json
import random

# Get the top "song_count" songs from every user passed in
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "uri", "song_data")
def get_users_top_songs(user_tokens: list = [], song_count: int = 100) -> dict:
    song_dict = {}
    print("Getting top songs for all users...")
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
            sys.exit(1)

        song_obj = response.json()
        # Parse request to get song data
        item_list = song_obj['items']
        for single_song in item_list:
            song_id = single_song["id"]
            song_uri = single_song["uri"]
            if song_id in song_dict:
                song_dict[song_id]["total_users"] += 1
            else: 
                song_dict[song_id] = {
                    "total_users": 1,
                    "uri": song_uri,
                    "song_data": single_song
                }
    print("Successfully got top songs for all users")
    return song_dict

# Get audio features for each song in the dictionary
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "uri", "song_data", "audio_features")
def get_audio_features(user_tokens: list = [], song_dict: dict = {}) -> dict:
    song_features = song_dict
    print("Getting audio features for all songs...")
    for song_id in song_dict:
        response = requests.get(
            f"https://api.spotify.com/v1/audio-features/{song_id}",
            headers={
                "Authorization": f"Bearer {user_tokens[random.randint(0, len(user_tokens)-1)]}"
            }
        )

        if response.status_code != 200:
            print(f"Failed to get audio features for songID ({song_id}): {response.json()}")
            sys.exit(1)

        song_response = response.json()
        song_features[song_id]["audio_features"] = song_response
    print("Successfully got audio features for all songs...")
    return song_features

# Rank songs by certain features
# Returns a max-heap for each category by score
# Each heap is indexed in a dict by category name
def rank_songs(songs_features: dict = {}, rank_categories: list = []) -> dict:
    category_heap = {}
    print("Starting to rank songs by category")
    for song_id in songs_features:
        for category in rank_categories:
            song_uri = songs_features[song_id]['uri']
            category_score = songs_features[song_id]["audio_features"][category]
            category_tuple = (-category_score, song_id, song_uri)
            if category in category_heap:
                heappush(category_heap[category], category_tuple)
            else:
                category_heap[category] = []
                heappush(category_heap[category], category_tuple)
    print("Successfully ranked all songs")
    return category_heap


# Gets top songs from each category
# Returns a list of songURIs for the final playlist
def get_top_category_songs(ranked_songs: dict = {}, total_songs: int = 100) -> list:
    song_arr = set()
    done = False
    while len(song_arr) < total_songs and not done:
        for category in ranked_songs:
            # Don't consider rest of categories if at the limit
            if len(song_arr) == total_songs:
                break
            # Don't consider empty categories
            elif len(ranked_songs[category]) == 0:
                continue

            song_uri = None
            skip_category = False
            # Pop from the heap until all duplicates are eliminated
            while song_uri is None or song_uri in song_arr:
                if len(ranked_songs[category]) == 0:
                    skip_category = True
                    break
                song_uri = heappop(ranked_songs[category])[2]

            if skip_category:
                continue
            song_arr.add(song_uri)
    return list(song_arr)



# Get the user profile and return the Spotify user ID
def get_user_id(token: str = "") -> str:
    user_res = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if user_res.status_code != 200:
        print(f"Failed to get user profile: {user_res.json()}")
        sys.exit(1)
    
    user_id = user_res.json()['id']
    return user_id



# Make the final spotify playlist from the songs
# Returns identifier of the new playlist
def make_final_playlist(user_tokens: list = [], final_songs: list = []) -> str:
    user_id = get_user_id(user_tokens[0])
    print(f"Making a new playlist for user {user_id}...")
    playlist_response = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers={
            "Authorization": f"Bearer {user_tokens[0]}"
        },
        data=json.dumps({
            "name": f"Spotify Smash {datetime.datetime.now().isoformat()}",
            "description": "A SUPER SMASHIN PLAYLIST",
            "public": "false",
            "collaborative": "true"
        })
    )
    if playlist_response.status_code != 200 and playlist_response.status_code != 201:
        print(f"Failed to make playlist: {playlist_response.json()}")
        sys.exit(1)

    playlist_id = playlist_response.json()["id"]
    print(f"Made playlist with ID: {playlist_id}")
    
    curr_song = 0
    print("Adding all songs to playlists...")
    while curr_song < len(final_songs):
        end_index = min(curr_song+99, len(final_songs))
        add_songs_res = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers={
                "Authorization": f"Bearer {user_tokens[0]}"
            },
            data=json.dumps({
                "uris": final_songs[curr_song:end_index]
            })
        )
        if add_songs_res.status_code != 200 and add_songs_res.status_code != 201:
            print(f"Failed to add songs to playlist: {add_songs_res.json()}")
            sys.exit(1)

        curr_song = end_index
    
    print("Successfully added all songs to playlist!")
    return playlist_id


# Add playlist to each user's account
def add_playlist_to_accounts(user_tokens: list = [], playlist_id: str = '') -> None:
    print("Adding playlists to user accounts")
    for i in range(1, len(user_tokens)):
        add_playlist_res = requests.put(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/followers",
            headers={
                "Authorization": f"Bearer {user_tokens[i]}"
            }
        )
        
        if add_playlist_res.status_code != 200:
            print(f"Failed to add playlist to user ({user_tokens[i]}): {add_playlist_res.json()}")
    print("Successfully added playlists to user accounts")


'''
token = ""
rank_categories = ["danceability", "energy", "acousticness"]
top_songs = get_users_top_songs([token], 5)
audio_features = get_audio_features([token], top_songs)
heap = rank_songs(audio_features, rank_categories)

song_list = []
for song in heap['energy']:
    my_uri = song[2]
    song_list.append(my_uri)

make_final_playlist(user_tokens=[token], final_songs=song_list)
'''

# Entry code and argument handling
if __name__ == "__main__":
    # Parse all arguments passed in
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokens", dest="tokens", metavar="T", type=str, required=True, help="Comma separated list of user Spotify tokens")
    parser.add_argument("--song-count", dest="songCount", metavar="C", type=int, required=True, help="Number of songs in the final playlist")
    parser.add_argument("--audio-features", dest="audioFeatures", metavar='AF', type=str, required=True, help="Comma separated list of audio features to optimize for in playlist.")
    parser.add_argument("--feature-weights", dest="featureWeights", metavar='W', type=str, required=False, help="Comma separated list of weights of each audio feature. Same ordering as features passed in.")
    arguments = parser.parse_args()
    tokens = arguments.tokens.split(',')
    song_count = arguments.songCount
    audio_features = arguments.audioFeatures.split(',')
    if arguments.featureWeights is not None:
        feature_weights = arguments.featureWeights.split(',')
        new_weights = []
        total_weight = 0.0
        for elem in feature_weights:
            total_weight += float(elem)
            new_weights.append(float(elem))

        if total_weight > 1:
            print("Weightings must add up to 100%!")
            sys.exit(1)
        feature_weights = new_weights
    else:
        feature_weights = [(1/len(audio_features))] * len(audio_features)


    print("==============Welcome to Spotify Smash!================")
    
    # =====================================================
    #              Start making the playlist
    # =====================================================
    # Get all the top songs for each user
    all_top_songs = get_users_top_songs(user_tokens=tokens, song_count=song_count)

    # Get the audio features of these songs
    all_audio_features = get_audio_features(user_tokens=tokens, song_dict=all_top_songs)

    # Rank all of the songs by category
    ranked_songs = rank_songs(songs_features=all_audio_features, rank_categories=audio_features)

    # Get the top songs from each category to add to the final playlist
    top_songs = get_top_category_songs(ranked_songs=ranked_songs, total_songs=song_count)

    # Make the playlist with all these songs for the first user
    final_playlist_id = make_final_playlist(user_tokens=tokens, final_songs=top_songs)

    # Make every other user subscribe to the final playlist
    add_playlist_to_accounts(user_tokens=tokens, playlist_id=final_playlist_id)

    print("======================SUCCESS==========================")
    print("A playlist has been created and added to your accounts!")