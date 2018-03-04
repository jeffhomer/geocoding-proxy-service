import urllib.request, json

### Generalized geolocation extractor ###
class GeolocationExtractor():
    
    # Extract geolocation from first working API
    @classmethod
    def getLocation(self,searchString):
        for apiservice in (hereAPI,googleAPI):
            location = apiservice.getLocation(searchString)
            if not location.status == -1:
                return location
        return location
    
    # Check status of all implemented APIs
    @classmethod
    def checkStatus(self):
        status={}
        for apiservice in (hereAPI,googleAPI):
            status[apiservice.API] = apiservice.getLocation("Canada")
        return status
    
### Location class with status and message attributes ###
class Location():
    status = -1
    message = ""
    location = [0.,0.]
    
    def __init__(self,status,message,location = None):
        self.status=status
        self.message=message
        if not location is None:
            self.location = location

# These are the getLocation() function implementations for each of the
# APIs (HERE, Google). You can add additional APIs by implementing them below
# and adding them to the for-loop in the GeolocationExtractor.getLocations() 
# function.

### HERE API ###
# If you regenerate the App ID and App Code, set the AppID and   AppCode 
# attributes appropriately
class hereAPI():
    AppID = "JDbEcowPNIAmQcE95vNz"
    AppCode = "09bySQ9I5aWOFiQGDbqbCQ"
    API = 'HERE'
    
    # Request the location of an address from the HERE API
    @classmethod
    def getLocation(self,searchString):
        # Construct and send request
        requestString = "https://geocoder.cit.api.here.com/6.2/geocode.json" \
                        + "?app_id=" + hereAPI.AppID \
                        + "&app_code=" + hereAPI.AppCode \
                        + "&searchtext=" + searchString        
        request = urllib.request.Request(requestString)        
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode())
        except:
            #ERROR: url request failed
            return Location(-1,constructError('URLRequest',self.API))
        
        # Get first location from response
        if (not response['Response']['View'] 
                or not response['Response']['View'][0]['Result']):
            #ERROR: invalid address
            return Location(-1,constructError('InvalidAddress',self.API))
        
        # Return location object
        location = response['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']        
        return Location(1,"OK",[location['Latitude'],location['Longitude']])
    
### Google API ###
# If you regenerate the Google API Key, set the Key attribute appropriately
class googleAPI():
    Key = "AIzaSyBwLb_44aG_osoWJWbP06qwtB2eJN4WbnE"
    API = 'Google'
    
    # Request the location of an address from the Google API
    @classmethod
    def getLocation(self,searchString):
        # Construct and send request
        requestString = "https://maps.googleapis.com/maps/api/geocode/json" \
                        + "?address=" + searchString \
                        + "&key=" + self.Key        
        request = urllib.request.Request(requestString)       
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode())
        except:
            #ERROR: url request failed
            return Location(-1,constructError('URLRequest',self.API))
        
        # Get first location from response
        if (not response['results'] 
                or not response['results'][0]['geometry']):
            #ERROR: invalid address
            return Location(-1,constructError('InvalidAddress',self.API))
        
        # Return location object
        location = response['results'][0]['geometry']['location']        
        return Location(1,"OK",[location['lat'],location['lng']])
    
# Construct relevant error using error ID and API type
def constructError(ID,API):
    if ID == 'URLRequest':
        return "ERROR: URL request failed ("+API+")."
    elif ID == 'InvalidAddress':
        return "ERROR: Address could not be found ("+API+")."