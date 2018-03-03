import http.server, sys
from geocodingservice import GeocodingServiceHTTPRequestHandler
        
if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8000
    MIRROR_RESPONSES = False
    
    # Input arguments
    if(len(sys.argv)>1):
        try:
            PORT = int(sys.argv[1])
        except:
            print("[PORT] must be an integer. Ex: 8000")
            sys.exit()
    if(len(sys.argv)>2):
        try:
            MIRROR_RESPONSES = bool(int(sys.argv[2]))
        except:
            print("[MIRROR_RESPONSES] must be an integer. Ex: 0/1")
            sys.exit()

    # Create the server
    server = http.server.HTTPServer((HOST, PORT), GeocodingServiceHTTPRequestHandler)
    server.mirror_responses = MIRROR_RESPONSES

    # Run the server until shut down
    server.serve_forever()