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

To run the geolocating service using default port 8000, call run_geolocating_service without any arguments:
```
> python run_geolocating_service.py
```
To select the port, use the first optional command-line argument ```[PORT]```:
```
> python run_geolocating_service.py [PORT]
```
To set a password to secure external shutdown commands, use the second optional command-line argument ```[PASSWORD]```:
```
> python run_geolocating_service.py [PORT] [PASSWORD]
```
The password must be alphanumeric and exactly 4 characters in length.

To mirror the client responses to the geolocating service, pass ```1``` to the third optional command-line argument ```[MIRROR_RESPONSES]```:
```
> python run_geolocating_service.py [PORT] [PASSWORD] [MIRROR_RESPONSES]
```

To shut the service down safely, send an external request to the server as described in [Stop server](https://github.com/jeffhomer/geocoding-proxy-service/blob/master/README.md#stop-server).

## How to Use the Services API
In the below examples, ```PORT``` refers to the port you set when running the service. If you did not select a port, the service uses a default port 8000.

### Search address:
Use the ```search``` method in a GET request to search for an address specified by ```SEARCHTEXT```. The service will first try to use the HERE API, and if that fails, will switch to the Google API. 
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

If none of the APIs locate the address successfully, the method will instead return a JSON message describing the error:
```
{
    "Message": "Location could not be obtained using any of the implemented APIs. Ensure that you are connected to the internet."
}
```

### Check status of API services:
To verify that the calls to the HERE and Google APIs are successful, use the ```check_api_status``` method in a GET request.
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
If any of the APIs are consistently failing, you may need to regenerate the API key(s). Once you have a regenerated or working key, you can modify the attribute in the appropriate API class in **geolocationextractor.py**. For example, for the Google API, look for the class ```googleAPI```:
```
### Google API ###
# If you regenerate the Google API Key, set the Key attribute appropriately
class googleAPI():
    Key = "IaMaRaNdOmLyGeNeRaTeDkEy"
    API = 'Google'
```

### Stop server: 
Use the ```shut_down``` method in a PUT request to shut down the service safely.
```
http://localhost:PORT/shut_down
```
The header must include the standard ```'Content-Length'```. If you set a password when creating the server, it must be included in the JSON-formatted request body:
```
{
	"password" : "1234"
}
```
If successful, the service will return a JSON-encoded message referencing the IP of the client before shutting down:
```
{
    "Message": "Server shut down by 127.0.0.1."
}
```
