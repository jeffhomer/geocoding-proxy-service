import http.server, json, threading, urllib
from geolocationextractor import GeolocationExtractor

### HTTP request handler for geocoding service ###
class GeocodingServiceHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
    ## Respond to a HEAD request ##
    def do_HEAD(self):
        # Respond to a HEAD request
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
              
    # Respond to a GET request
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Parse url and call appropriate method
        parsedUrl = urllib.parse.urlparse(self.path)
        if parsedUrl.path == '/search':       
            self.searchAddress(parsedUrl)
        elif parsedUrl.path == '/check_api_status':
            self.checkStatus()
        else:
            self.respond({"Message": "Did not recognize function. Please use /search to search for an address or /check_api_status to verify connection with external APIs."})

    # Respond to a POST request
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Make sure content length is included in header
        if not ('Content-Length' in self.headers):
            self.respond({"Message": "Header 'Content-Length' not found. Ensure that clients include this in PUT requests."})
            return
        
        # Parse url and call appropriate method
        parsedUrl = urllib.parse.urlparse(self.path)
        if parsedUrl.path == '/shut_down':
            self.serverShutdownSecure(self.rfile.read(int(self.headers['Content-Length'])))
    
    # Shut down server and notify client
    def serverShutdown(self):
        self.respond({"Message":"Server shut down by " + self.address_string() + "."})
        t = threading.Thread(target = self.server.shutdown)
        t.daemon = True
        t.start()
        
    # Secure shutdown
    def serverShutdownSecure(self,postBody):
        # If no password, shut down
        if(not self.server.password):
            self.serverShutdown()
            return
        
        try:
            data = json.loads(postBody)
        except:
            self.respond({"Message":"Invalid control character in request body. Please reconstruct your request and try again."})
            return
        if (not 'password' in data) or (not data['password'] == self.server.password):
            self.respond({"Message": "Invalid password. Ensure that your request body includes the password set by your server administrator."})
        else:
            self.serverShutdown()
        
    # Get latitude and longitude of searched address
    def searchAddress(self,parsedUrl):
        # Parse query for search string
        queries = urllib.parse.parse_qs(parsedUrl.query)
        if not 'address' in queries:
            # ERROR: invalid query
            self.respond({"Message": "Invalid query. Please make sure to follow the format 'address=SEARCHTEXT' and that SEARCHTEXT is plus-encoded"})
            return
        
        # Get location from one of the APIs
        searchString = urllib.parse.quote_plus(queries['address'][0])
        location = GeolocationExtractor.getLocation(searchString)      
        if location.status == -1:
            # ERROR: cannot get location
            self.respond({"Message": "Location could not be obtained using any of the implemented APIs. Ensure that you are connected to the internet."})
            return
        self.respond({"latitude": location.location[0], "longitude": location.location[1]})
        
    # Check status of all implemented APIs
    def checkStatus(self):
        location = GeolocationExtractor.checkStatus()
        status={}
        for api in location:
            if location[api].status == -1:
                status_i = "ERROR"
            else:
                status_i = "OK"
            status[api] = status_i
        self.respond(status)
        
    # Respond to client and mirror to server if MIRROR_RESPONSES is true
    def respond(self,message):
        self.wfile.write(json.dumps(message).encode('utf-8'))
        if self.server.mirror_responses:
            print(message)