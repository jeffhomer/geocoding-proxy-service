import http.server, json, threading, urllib
from geolocationextractor import GeolocationExtractor

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
        if not 'address' in queries:
            # ERROR: invalid query
            self.wfile.write(json.dumps({"Message": "Invalid query. Please make sure to follow the format 'address=SEARCHTEXT' and that SEARCHTEXT is plus-encoded"}).encode('utf-8'))
            return
        
        # Get location from one of the APIs
        searchString = urllib.parse.quote_plus(queries['address'][0])
        location = GeolocationExtractor.getLocation(searchString)      
        if location == -1:
            # ERROR: cannot get location
            self.wfile.write(json.dumps({"Message": "Could not retrieve location from any API. Please make sure you are connected to the internet."}).encode('utf-8'))
            return
        self.wfile.write(json.dumps({"latitude": location[0], "longitude": location[1]}).encode('utf-8'))