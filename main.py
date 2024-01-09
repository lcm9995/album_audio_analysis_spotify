
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import matplotlib.pyplot as plt
import random as random

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) 
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query=f"?q={artist_name}&type=artist&limit=1"
    query_url = url+query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result[0]

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_songs_on_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_track_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

def choose_album(album_response):
    for item in album_response:
        print(item['name'])
    album_name = input("\nType one of the above album's names (case sensitive): ").strip()
    for item in album_response:
        if item['name']==album_name:
            album = item
    return album

def get_audio_feature_from_user(audio_feature_options): 
    print("\n Audio Features for Visual Analysis: \n")
    print(audio_feature_options)
    # print("Audio Features for Visual Analysis:\n'danceability', \n'energy', \n'liveness', \n'loudness', \n'speechiness', \n'tempo', \n'valence' \n")
    feature = input("Please choose one of the above audio features to view and type it in (case sensitive): ").strip()
    return feature

def select_audio_feature():
    audio_feature_options = ['danceability', 'energy', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    feature = get_audio_feature_from_user(audio_feature_options)
    while(feature not in audio_feature_options):
        print("Response doesn't match an audio features option, please try again")
        feature = get_audio_feature_from_user()
    return feature

def main():
    token = get_token()
    artist_name = input("Please enter the name of an artist on spotify: ")
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]

    albums_response = get_albums_by_artist(token, artist_id)['items']
    album = choose_album(albums_response)
    album_name = album['name']
    album_tracks = get_songs_on_album(token, album['id'])

    tracks_dict = {}
    for item in album_tracks['items']:
        track_analysis = get_track_audio_features(token, item['id'])
        tracks_dict[item['name']]=track_analysis
    
    feature = select_audio_feature()
    song_names = []
    song_stats = []
    for key in tracks_dict:
        song_names.append(key)
        song_stats.append(tracks_dict[key][feature])
    plt.scatter(song_names, song_stats, color = get_random_color())
    plt.title(artist_name + "'s " + album_name + ": " + feature)
    plt.show()

main()


