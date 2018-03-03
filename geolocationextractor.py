import urllib, json

class GeolocationExtractor():
    """ Abstract class for geolocation extraction """
    
    @classmethod
    def getLocation(self,searchString):
        for apiservice in (googleAPI,hereAPI):
            location = apiservice.getLocation(searchString)
            if not location == -1:
                return location
        return location

class hereAPI():
    AppID = "JDbEcowPNIAmQcE95vNz"
    AppCode = "09bySQ9I5aWOFiQGDbqbCQ"
    
    @classmethod
    def getLocation(self,searchString):
        requestString = "https://geocoder.cit.api.here.com/6.2/geocode.json" \
                        + "?app_id=" + hereAPI.AppID \
                        + "&app_code=" + hereAPI.AppCode \
                        + "&searchtext=" + searchString
        
        request = urllib.request.Request(requestString)
        
        response = json.loads(urllib.request.urlopen(request).read().decode())
        
        # Get first location
        if not response['Response']['View']:
            #ERROR
            return -1
        elif not response['Response']['View'][0]['Result']:
            #ERROR
            return -1
        
        # Return display location
        location = response['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']        
        return location
    
class googleAPI():
    Key = "AIzaSyBwLb_44aG_osoWJWbP06qwtB2eJN4WbnE"
    
    @classmethod
    def getLocation(self,searchString):
        requestString = "https://maps.googleapis.com/maps/api/geocode/json" \
                        + "?address=" + searchString \
                        + "&key=" + self.Key
        
        request = urllib.request.Request(requestString)
        
        response = json.loads(urllib.request.urlopen(request).read().decode())
        
        # Get first location
        if not response['results']:
            #ERROR
            return -1
        elif not response['results'][0]['geometry']:
            #ERROR
            return -1
        
        # Return display location
        location = response['results'][0]['geometry']['location']        
        return location