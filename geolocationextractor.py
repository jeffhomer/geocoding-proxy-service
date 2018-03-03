import urllib.request, json

class GeolocationExtractor():
    """ Extract geolocation from first working API """
    
    @classmethod
    def getLocation(self,searchString):
        for apiservice in (hereAPI,googleAPI):
            location = apiservice.getLocation(searchString)
            if not location == -1:
                return location
        return location
    
    @classmethod
    def checkStatus(self):
        status={}
        for apiservice in (hereAPI,googleAPI):
            status[apiservice.API] = apiservice.getLocation("Canada")
        return status

""" These are the getLocation() function implementations for each of the
APIs (HERE, Google). You can add additional APIs by implementing them below
and adding them to the for-loop in the GeolocationExtractor.getLocations() 
function, above """

class hereAPI():
    AppID = "JDbEcowPNIAmQcE95vNz"
    AppCode = "09bySQ9I5aWOFiQGDbqbCQ"
    API = 'HERE'
    
    @classmethod
    def getLocation(self,searchString):
        # Request from API
        requestString = "https://geocoder.cit.api.here.com/6.2/geocode.json" \
                        + "?app_id=" + hereAPI.AppID \
                        + "&app_code=" + hereAPI.AppCode \
                        + "&searchtext=" + searchString        
        request = urllib.request.Request(requestString)        
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode())
        except:
            #ERROR: url request failed
            printError('URLRequest',self.API)
            return -1
        
        # Get first location
        if (not response['Response']['View'] 
                or not response['Response']['View'][0]['Result']):
            #ERROR: invalid address
            printError('InvalidAddress',self.API)
            return -1
        
        # Return display location
        location = response['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']        
        return [location['Latitude'],location['Longitude']]
    
class googleAPI():
    Key = "AIzaSyBwLb_44aG_osoWJWbP06qwtB2eJN4WbnE"
    API = 'Google'
    
    @classmethod
    def getLocation(self,searchString):
        # Request from API
        requestString = "https://maps.googleapis.com/maps/api/geocode/json" \
                        + "?address=" + searchString \
                        + "&key=" + self.Key        
        request = urllib.request.Request(requestString)       
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode())
        except:
            #ERROR: url request failed
            printError('URLRequest',self.API)
            return -1
        
        # Get first location
        if (not response['results'] 
                or not response['results'][0]['geometry']):
            #ERROR: invalid address
            printError('InvalidAddress',self.API)
            return -1
        
        # Return display location
        location = response['results'][0]['geometry']['location']        
        return [location['lat'],location['lng']]
    
def printError(ID,API):
    # Print relevant error
    if ID == 'URLRequest':
        print("ERROR: URL request failed ("+API+").")
    elif ID == 'InvalidAddress':
        print("ERROR: Address could not be found ("+API+").")