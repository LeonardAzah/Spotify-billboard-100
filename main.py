from bs4 import  BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

response = requests.get(url=billboard_url)
response.raise_for_status()
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
songs = soup.select(selector="li h3")
titles = [title.getText().strip() for title in songs]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username="Leonard"
    )
)

user_id = sp.current_user()['id']
playlist_urls = []
for song in titles:
    spotify_results = sp.search(q=f"track: {song} year: 2014")
    try:
        url = spotify_results["tracks"]["items"][0]["uri"]
        playlist_urls.append(url)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

my_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Tracks", public=False,
                                     description="Top Tracks"  )
playlist = playlist_urls[:100]
sp.playlist_add_items(playlist_id=my_playlist["id"] , items=playlist,position=None)