from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = "be242dbe02ee457ba11ebf852747929a"
Client_Secret = "e90e214311a64d74b7f5892ef0906bf9"
URL = "https://www.billboard.com/charts/hot-100/"


# Scraping Billboard Top 100

date = input("What year do you want to travel to? Type the date in YYYY-MM-DD format: ")

response = requests.get(URL + date)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

top_song = soup.find_all(
    name="span", class_="chart-element__information__song text--truncate color--primary"
)
top_song_title = [song.getText() for song in top_song]

# top_artists = soup.find_all(
#     name="span", class_="chart-element__information__artist text--truncate color--secondary"
# )
# top_song_artists = [artist.getText() for artist in top_artists]

print(top_song_title)
# print(top_song_artists)

# Spotify Authentication

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()['id']
print(user_id)

# Searching Spotify for songs by title

song_uris = []
year = date.split("-")[0]
print(year)

for song in top_song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboar 100", public=False)
print(playlist)

#Adding songs found into playlist

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)