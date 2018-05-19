import json
import urllib.request
import urllib.parse
import shared_data


def execute():
    print('Playing lastFm - similar')

    artist = shared_data.data['lastFm']['artist']
    # artist = 'Wanting'
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist='+artist+'&limit=1&api_key=bff8bc4f35aa20038d8cccf7e70c5ff8&format=json'
    html_content = urllib.request.urlopen(url)
    topTracks = html_content.read().decode()
    topt = json.loads(topTracks)

    track = topt['toptracks']['track'][0]['name']

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist='+artist+'&track='+track+'&limit=100&api_key=bff8bc4f35aa20038d8cccf7e70c5ff8&format=json'
    html_content = urllib.request.urlopen(url)
    simTracks = html_content.read().decode()
    simt = json.loads(simTracks)
    # print(str(simt))

    tracks = [i['artist']['name'] + ' - '+ i['name'] for i in simt['similartracks']['track']]
    shared_data.data['playlist'].extend([{'title': t} for t in tracks])

    shared_data.objects['youtubeLinker'].runThread()

