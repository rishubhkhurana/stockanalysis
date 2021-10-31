import requests

urls = {
    'pcr': 'https://options.icharts.in/opt/PutCallOITotal.php',

}

def get_icharts_urls():
    return list(urls.values())

def get_icharts_keys():
    return list(urls.keys())

def get_icharts_url(key:str)->str:
    return urls[key]

def get_icharts_data(url, header=None):
    try:
        content = requests.get(url, header=header)
        return content
    except:
        return "Unable to extract data"