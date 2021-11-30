import codecs
import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials

spot = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id="dcffc14978ed497aa58834a7864a99b7", client_secret="e8c5cc78c8e74ccd92323d146c635b47"))

def get_artista_por_nome(name):
    busca = spot.search(name)
    items = busca['tracks']['items']
    if len(items) > 0:
        return items[0]['artists'][0]
    else:
        return None

def get_id_do_artista(artist):
    return artist['id']

def get_dados_do_artista(id): 
  albuns_do_artista = spot.artist_albums(id, limit=50)
  albuns = {}

  for i in range(len(albuns_do_artista['items'])):
    id = albuns_do_artista['items'][i]['id']
    name = albuns_do_artista['items'][i]['name']
    albuns[id] = name

  return albuns

def get_dados_dos_albuns(album_id, album_name):
  spotify_album = {}
  
  tracks = spot.album_tracks(album_id)  
  album = spot.album(album_id)

  for n in range(len(tracks['items'])):
    id_track = tracks['items'][n]['id']
    track = spot.track(id_track)
    features = spot.audio_features(id_track)
    spotify_album[id_track] = {}

    spotify_album[id_track]['album'] = album_name 
    spotify_album[id_track]['track_number'] = track['track_number'] 
    spotify_album[id_track]['name'] = track['name'] 
    spotify_album[id_track]['popularity'] = track['popularity'] 
    spotify_album[id_track]['duration_ms'] = track['duration_ms']	    
    spotify_album[id_track]['danceability'] = features[0]['danceability']
    spotify_album[id_track]['valence'] = features[0]['valence']
    spotify_album[id_track]['release_date'] = album['release_date']

  return spotify_album

def get_dados_de_todos_albuns(albums_ids_names):
  spotify_albums = []
  albums_names = []
  for id, name in albums_ids_names.items():
    if name.lower() not in albums_names:
      albums_names.append(name.lower())
      dados_dos_albuns = get_dados_dos_albuns(id,name) 
      for item in dados_dos_albuns.items():
        spotify_albums.append(item[1]) 

  return spotify_albums

def convert_to_csv(filepath, name):
  keys = filepath[0].keys()
  print(keys)
  csv_name = ''+ name + '.csv'
  output_file = codecs.open(csv_name, 'w', encoding = 'utf-8')
  dict_writer = csv.DictWriter(output_file, keys)
  dict_writer.writeheader()
  dict_writer.writerows(filepath)
  output_file.close()  
  return


name = "BTS"

artista = get_artista_por_nome(name)    

#Se encontrar o artista no spotify:
if artista:
    id_do_artista = get_id_do_artista(artista)
    dados_do_artista = get_dados_do_artista(id_do_artista)
    dados_dos_albuns = get_dados_de_todos_albuns(dados_do_artista)
    convert_to_csv(dados_dos_albuns, 'musicas')   

else:
    logger.error("Can't find artist: %s", artista)

