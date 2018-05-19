import json
import urllib.request
import urllib.parse
import shared_data


def execute():
    print('Playing lastFm - top')

    # artist = shared_data.data['lastFm']['artist']
    url = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag='+artist+'&limit=100&api_key=bff8bc4f35aa20038d8cccf7e70c5ff8&format=json'
    print(url)

    html_content = urllib.request.urlopen(url)
    topTracks = html_content.read().decode()
    topt = json.loads(topTracks)

    print(str(topt))

    tracks = [i['artist']['name'] + ' - '+ i['name'] for i in topt['tracks']['track']]
    shared_data.data['playlist'].extend([{'title': t} for t in tracks])

    shared_data.objects['youtubeLinker'].runThread()

