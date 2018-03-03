import http.server
from geocodingservice import GeocodingServiceHTTPRequestHandler
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8004

    # Create the server
    server = http.server.HTTPServer((HOST, PORT), GeocodingServiceHTTPRequestHandler)

    # Run the server until shut down
    server.serve_forever()