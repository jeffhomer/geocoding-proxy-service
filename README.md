# Geocoding Proxy Service
Network service that resolves latitude and longitude coordinates for a given address

## Contents
1. [Requirements](https://github.com/jeffhomer/geocoding-proxy-service/blob/master/README.md#requirements)
2. [How to Run the Service](https://github.com/jeffhomer/geocoding-proxy-service/blob/master/README.md#how-to-run-the-service)
3. [How to Use the Services API](https://github.com/jeffhomer/geocoding-proxy-service/blob/master/README.md#how-to-use-the-services-api)

## Requirements
Before using the geocoding proxy service, please ensure you are using Python 3.6.4, and that it is available on the system path.

## How to Run the Service
Open a command window or terminal in the directory containing **run_geolocating_service.py**.

To run the geolocating service using default port 8000, run:
```
> python run_geolocating_service
```

To select the port, use the first optional command-line argument [PORT]:
```
> python run_geolocating_service [PORT]
```

To mirror the client responses to the geolocating service, pass ```True``` to the second optional command-line argument [MIRROR_RESPONSES]:
```
> python run_geolocating_service [PORT] [MIRROR_RESPONSES]
```

To shut down the service safely, send an external request to the server as described in [Stop server](https://github.com/jeffhomer/geocoding-proxy-service/blob/master/README.md#stop-server).

## How to Use the Services API
In the below examples, ```PORT``` refers to the port you set when running the service. If you did not select a port, the service uses a default port 8000.

### Search address:
Use the ```search``` method to search for an address specified by ```SEARCHTEXT```. The service will first try to use the HERE API, and if that fails, will switch to the Google API. 
```
http://localhost:PORT/search?address=SEARCHTEXT
```
This will return a JSON object with the form:
```
{
    "latitude": 49.15796,
    "longitude": -123.18759
}
```
Ensure that ```SEARCHTEXT``` follows the regular encoding for URL queries; that is, spaces should be replaced by plus signs, and special characters by ```%xx``` escapes. You can use ```urllib.parse.quote_plus``` in python to encode a regular string accordingly.

### Stop server: 
Use the ```shut_down``` method to shut down the service safely.
```
http://localhost:PORT/shut_down
```
This will return a JSON-encoded message referencing the IP of the client that shut down the service:
```
{
    "Message": "Server shut down by 127.0.0.1."
}
```

### Check status of API services
To verify that the calls to the HERE and Google APIs are successful, use the ```check_api_status``` method.
```
http://localhost:PORT/check_api_status
```
This will return a JSON-encoded status with the form:
```
{
    "HERE": "OK",
    "Google": "FAILED"
}
```
