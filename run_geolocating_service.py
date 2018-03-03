import http.server, sys
from geocodingservice import GeocodingServiceHTTPRequestHandler
        
if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8000
    MIRROR_RESPONSES = False
    
    # Input arguments
    if(len(sys.argv)>1):
        PORT = int(sys.argv[1])
    if(len(sys.argv)>2):
        MIRROR_RESPONSES = bool(sys.argv[2])

    # Create the server
    server = http.server.HTTPServer((HOST, PORT), GeocodingServiceHTTPRequestHandler)
    server.mirror_responses = MIRROR_RESPONSES

    # Run the server until shut down
    server.serve_forever()