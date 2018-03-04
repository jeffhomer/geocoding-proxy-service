import http.server, sys
from geocodingservice import GeocodingServiceHTTPRequestHandler

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8000
    MIRROR_RESPONSES = False
    PASSWORD = None
    
    # Input arguments
    if(len(sys.argv)>1):
        try:
            PORT = int(sys.argv[1])
        except:
            print("[PORT] must be an integer. Ex: 8000")
            sys.exit()
    if(len(sys.argv)>2):
        if (not len(sys.argv[2])==4) or (not sys.argv[2].isalnum()):
            print("[PASSWORD] must be alphanumeric and contain exactly 4 characters.")
            sys.exit()
        PASSWORD = sys.argv[2]    
    if(len(sys.argv)>3):
        try:
            MIRROR_RESPONSES = bool(int(sys.argv[3]))
        except:
            print("[MIRROR_RESPONSES] must be an integer. Ex: 0/1")
            sys.exit()

    # Create the server
    server = http.server.HTTPServer((HOST, PORT), GeocodingServiceHTTPRequestHandler)
    server.mirror_responses = MIRROR_RESPONSES
    server.password = PASSWORD

    # Run the server until shut down
    print("Geolocating service has been started.")
    server.serve_forever()