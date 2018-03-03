import http.server, json, threading, urllib

class GeocodingServiceHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """ HTTP request handler for geocoding service """

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
    def do_GET(self):
        # Respond to a GET request
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Parse path for function call
        parsedUrl = urllib.parse.urlparse(self.path)
        if parsedUrl.path == '/shut_down':
            self.serverShutdown()
        elif parsedUrl.path == '/search':       
            self.searchAddress(parsedUrl)
        else:
            self.wfile.write(json.dumps({"Error": "Did not recognize function. Please use /search to search for an address or /shut_down to shut down the server"}).encode('utf-8'))

    def serverShutdown(self):
        # Shut down server and notify client
        self.wfile.write(json.dumps({"Message":"Server shutting down."}).encode('utf-8'))
        clientAddress = self.address_string()
        t = threading.Thread(target = self.server.shutdown)
        t.daemon = True
        t.start()
        print("Server shutting down by " + clientAddress)
        
    def searchAddress(self,parsedUrl):
        # Parse query for search string
        queries = urllib.parse.parse_qs(parsedUrl.query)
        if 'address' in queries:
            print(hereAPI.getAddress(urllib.parse.quote_plus(queries['address'][0])))
        else:
            print(0)        
        self.wfile.write(json.dumps({"latitude": 0, "longitude": 0}).encode('utf-8'))
        
class hereAPI:
    AppID = "JDbEcowPNIAmQcE95vNz"
    AppCode = "09bySQ9I5aWOFiQGDbqbCQ"
    
    @classmethod
    def getAddress(self,searchString):
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
    
class googleAPI:
    Key = "AIzaSyBwLb_44aG_osoWJWbP06qwtB2eJN4WbnE"
    
    @classmethod
    def getAddress(self,searchString):
        requestString = "https://maps.googleapis.com/maps/api/geocode/json" \
                        + "?address=" + searchString \
                        + "&key=" + self.Key
        
        request = urllib.request.Request(requestString)
        
        return urllib.request.urlopen(request).read().decode()