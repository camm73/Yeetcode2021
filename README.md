# Spotify Smash
Spotify Smash is an automated playlist generator for Spotify that aggregates the top songs from a list of users, ranks the songs based on certain audio features (e.g. "danceability"), and generates a private, collaborative playlist to share with all the users.

## Usage
`python3 spotify_smash.py --tokens {comma seperated list of Spotify OAuth Tokens} --song-count {number of songs in the final playlist} --audio-features {audio features to optimize for}`

Valid audio features are: `acousticness`, `danceability`, `energy`, `duration_ms`, `instrumentalness`, `liveness`, `speechiness`, `tempo`, and `valence`.


## Future Features
* Allow maximization or minimization choice for each feature (currently each feature is maximized)
* Allow for more than 50 songs selected from each person
* Allow for varied "lookback" windows on user's popular songs
* Set percentage of each audio feature's contribution to the final playlist
