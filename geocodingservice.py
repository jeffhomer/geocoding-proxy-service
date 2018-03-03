import http.server, json, threading, urllib
from geolocationextractor import GeolocationExtractor

class GeocodingServiceHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """ HTTP request handler for geocoding service """

    def do_HEAD(self):
        # Respond to a HEAD request
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
    def do_GET(self):
        # Respond to a GET request
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Call appropriate method
        parsedUrl = urllib.parse.urlparse(self.path)
        if parsedUrl.path == '/shut_down':
            self.serverShutdown()
        elif parsedUrl.path == '/search':       
            self.searchAddress(parsedUrl)
        elif parsedUrl.path == '/check_api_status':
            self.checkStatus()
        else:
            self.respond({"Message": "Did not recognize function. Please use /search to search for an address or /shut_down to shut down the server."})

    def serverShutdown(self):
        # Shut down server and notify client
        self.respond({"Message":"Server shut down by " + self.address_string() + "."})
        t = threading.Thread(target = self.server.shutdown)
        t.daemon = True
        t.start()
        
    def searchAddress(self,parsedUrl):
        # Get latitude and longitude of searched address
        
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
        
    def checkStatus(self):
        # Check status of all APIs
        location = GeolocationExtractor.checkStatus()
        status={}
        for api in location:
            if location[api].status == -1:
                status_i = "ERROR"
            else:
                status_i = "OK"
            status[api] = status_i
        self.respond(status)
        
    def respond(self,message):
        # Respond to client
        self.wfile.write(json.dumps(message).encode('utf-8'))
        if self.server.mirror_responses:
            print(message)