import requests
from io import BytesIO

class UrlBytes():

    def __init__(self, url):
        if url.startswith('//'):
            url= "https:"+url
        elif url.startswith('www'):
            url= "https://"+url
        elif url.startswith('https:http:/'):
            url= url.replace('http:', '')
        elif url.startswith('-|'):
            url= url.replace('-|', '')
        self.url= url

    def getUrlResponse(self):  
        try:
            header={
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"} 
            response= requests.get(self.url, timeout=10, headers= header)
            if response.status_code == 422:
                url= url.replace('http','https')
                response= requests.get(url, timeout=10, headers= header)
            elif response.status_code == 403:
                return False, 'FORBIDDEN'
            elif response.status_code == 404:
                return False, 'BROKEN 404'
            return True, BytesIO(response.content)
        except:
            return False, 'BROKEN'  
            
    def getLocalResponse(self):
        try:
            with open(self.url, 'rb') as source_file:
                # Read all bytes from the source file
                image_data = source_file.read()
                return True, BytesIO(image_data)
        except:
            return False, 'BROKEN PATH' 

    def getImageBytes(self):
        if self.url.startswith('\\') or self.url.__contains__('C:\\'):
            reponse= self.getLocalResponse()
        else:
            reponse=  self.getUrlResponse()
        return reponse
        