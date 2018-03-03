import http.server
import json
import urllib

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
        else if not response['Response']['View'][0]['Result']:
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

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Custom HTTP request handler
    
    Implement head and get methods
    """

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
    def do_GET(self):
        # Respond to a GET request
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        # Parse query for search string
        parsedUrl = urllib.parse.urlparse(self.path)
        queries = urllib.parse.parse_qs(parsedUrl.query)
        if 'address' in queries:
            print(hereAPI.getAddress(urllib.parse.quote_plus(queries['address'][0])))
        else:
            print(0)
        
        self.wfile.write(json.dumps({"latitude": 0, "longitude": 0}).encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8003

    # Create the server
    server = http.server.HTTPServer((HOST, PORT), MyHTTPRequestHandler)

    # Run the server until interrupted with ctrl+c
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()