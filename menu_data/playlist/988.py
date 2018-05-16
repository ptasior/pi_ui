import shared_data

def execute():
    print('Playing 988')
    shared_data.data['playlist'].append({
            'title': '988',
            'url' : 'http://starrfm.rastream.com:80/starrfm-988'
        })

