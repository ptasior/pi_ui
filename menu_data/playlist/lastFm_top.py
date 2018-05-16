import json
import urllib.request
import urllib.parse
import shared_data


def execute():
    print('Playing lastFm - top')

    artist = shared_data.data['lastFm']['artist']
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist='+artist+'&api_key=bff8bc4f35aa20038d8cccf7e70c5ff8&format=json'
    html_content = urllib.request.urlopen(url)
    topTracks = html_content.read().decode()
    topt = json.loads(topTracks)

    tracks = [i['artist']['name'] + ' - '+ i['name'] for i in topt['toptracks']['track']]
    shared_data.data['playlist'].extend([{'title': t} for t in tracks])

    shared_data.objects['youtubeLinker'].runThread()

