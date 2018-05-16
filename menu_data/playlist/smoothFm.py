import shared_data

def execute():
    print('Playing SmoothFM')
    shared_data.data['playlist'].append({
            'title': 'Smooth FM',
            'url' :'http://streaming.novaentertainment.com.au/smooth915'
        })

