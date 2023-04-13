import schedule
import time
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from src.skype import SkypeCustom as Skype
from src.mattermost import Mattermost
from dotenv import load_dotenv
import platform
my_os = platform.system()

# get .env
load_dotenv()

os.environ["SPOTIPY_CLIENT_ID"] = os.getenv('SPOTIPY_CLIENT_ID')
os.environ["SPOTIPY_CLIENT_SECRET"] = os.getenv('SPOTIPY_CLIENT_SECRET')

# Set up authorization and initialize client
scope = "user-read-playback-state"

# capath exists on windows but not on linux

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri='http://localhost:8000/callback', 
        cache_path='/home/phong/entertainment/spotify-synchronize/cache.txt' if my_os == 'Linux' else 'cache.txt'))

# set up for skype
username = os.getenv('SKYPE_USERNAME')
password = os.getenv('SKYPE_PASSWORD')
sk = Skype()
sk.conn.liveLogin(username, password)

# set up for mattermost
mattermost_server = os.getenv('MATTERMOST_SERVER')
mattermost_username = os.getenv('MATTERMOST_USERNAME')
mattermost_password = os.getenv('MATTERMOST_PASSWORD')
mm = Mattermost(mattermost_server, mattermost_username, mattermost_password)
mm.login()

previous_song = None


def get_current_song():
    global previous_song

    # Get current playback information
    current_playback = sp.current_playback()

    # Check if there is currently a song playing
    if current_playback is None or "item" not in current_playback or not current_playback[
            "is_playing"]:
        print("No song is currently playing.")
        if previous_song is not None:
            previous_song = None
            mm.remove_status()
            sk.setMood("")
            print("Mood set to empty")
    else:
        current_song = current_playback["item"]
        if current_song == previous_song:
            return
        # Extract song information
        song_name = current_playback["item"]["name"]
        artists = current_playback["item"]["artists"]
        artist_names = [artist["name"] for artist in artists]
        album_name = current_playback["item"]["album"]["name"]

        # Set previous song to current song
        previous_song = current_song

        # set status for mattermost
        mm.set_status(
            "online",
            "spotify", f"Playing: {song_name} by " +
            ', '.join(artist_names))
        # set mood for skype
        sk.setMood(mood="smile", text="Spotify: " +
                   song_name +
                   " by " +
                   ', '.join(artist_names))
        print("Mood set to: " + song_name + " by " + ', '.join(artist_names))


schedule.every(5).seconds.do(get_current_song)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    print(e)
    mm.remove_status()
    sk.setMood("")