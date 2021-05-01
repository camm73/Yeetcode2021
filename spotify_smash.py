import requests
import argparse

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
def get_audio_features(user_tokens: list = [], initial_songs: dict = {}) -> dict:
    pass

# expect dictinoary with key with song ID & another dictionary with total users + song data
# add new key thats audio features with values 

# Rank songs by certain features
# Returns a max-heap for each category by score
# Each heap is indexed in a dict by category name
def rank_songs(songs_with_features: dict = {}, rank_categories: list = []) -> dict:
    pass

# key: song ID (uri) - for loop 
# songs_with_features[songID][‘audio_features’]


# Gets top songs from each category
# Returns a list of songs for the final playlist
def get_top_category_songs(total_songs: int = 100) -> list:
    pass


# Make the final spotify playlist from the songs
# Returns identifier of the new playlist
def make_final_playlist(user_tokens: list = [], final_songs: list = []) -> str:
    pass


# Add playlist to each user's account
def add_playlist_to_accounts(user_tokens: list = [], playlist_id: str = '') -> None:
    pass


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
        for elem in feature_weights:
            new_weights.append(float(elem))
        feature_weights = new_weights
    else:
        feature_weights = [(1/len(audio_features))] * len(audio_features)
    
    print(feature_weights)