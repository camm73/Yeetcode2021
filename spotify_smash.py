import requests


# Get the top "song_count" songs from every user passed in
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "song_data")
def get_users_top_songs(user_tokens: list = [], song_count: int = 100) -> dict:
    song_dict = {}
    for token in user_tokens:
        # TODO: Make request for user's top songs

        # TODO: Parse request to get song data

        # TODO: Add to dictionary (or increment "total_users" field if it already exists)
        pass
    return song_dict


# Get audio features for each song in the dictionary
# Returns a dictionary from songID ("key") to another dictionary with keys ("total_users", "song_data", "audio_features")
def get_audio_features(user_tokens: list = [], initial_songs: dict = {}) -> dict:
    pass

# Rank songs by certain features
# Returns a max-heap for each category by score
# Each heap is indexed in a dict by category name
def rank_songs(songs_with_features: dict = {}, rank_categories: list = []) -> dict:
    pass


# Gets top songs from each category
# Returns a list of songs for the final playlist
def get_top_category_songs(total_songs: int = 100) -> list:
    pass


# Make the final spotify playlist from the songs
# Returns identifier of the new playlist
def make_final_playlist(user_tokens: list = [], user_tokensfinal_songs: list = []) -> str:
    pass


# Add playlist to each user's account
def add_playlist_to_accounts(user_tokens: list = [], playlist_id: str = '') -> None:
    pass


# Entry code and argument handling
if __name__ == "__main__":
    pass