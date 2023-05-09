# -----------------------------------------imports-----------------

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth


# -----------------------------------------Getting a request from the billboard website-----------------

date = input("What year would you like to travel to?:YYYY-MM-DD ")
billboard_endpoint = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(billboard_endpoint)
content = response.text
# -----------------------------------------Scraping the website-----------------

soup = BeautifulSoup(content, "html.parser")
all_songs = soup.select("li ul li h3")
song_list = [song.getText().strip() for song in all_songs]
print(song_list)

# -----------------------------------------Creating a playlist in spotify-----------------

CLIENT_ID = "82955b6a802b44e4935056f57bc8801d"
CLIENT_SECRET = "24c91170886546f0ab89104254b9d44d"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)


# -----------------------------------------Adding songs to the playlist-----------------


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
