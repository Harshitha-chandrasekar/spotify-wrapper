import os
from flask import Flask, redirect, request, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Spotify credentials from environment
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "user-top-read user-read-recently-played"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    token_info = session.get("token_info")
    if not token_info:
        return redirect(url_for('login'))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=5, time_range='short_term')
    
    artists = [artist['name'] for artist in top_artists['items']]
    return render_template('dashboard.html', artists=artists)

if __name__ == '__main__':
    app.run(debug=True)
