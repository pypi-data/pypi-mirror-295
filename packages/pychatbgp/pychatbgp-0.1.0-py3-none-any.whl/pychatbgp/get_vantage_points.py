import requests

def get_vantage_points( \
    ip_protocol=None, \
    vantage_points=None):
    
    """
    Calls the ChatBGP API and returns the response.

    Parameters:
    ip_protocol (str): The IP protocol version. It can be 'ipv4' or 'ipv6' (default is both).
    vantage_points (str): String with the VPs identified by their IP (comma separated). Only VPs in the list can be returned.

    Returns:
    dict: The response from the API in JSON format.
    """

    url = "http://130.79.48.56:8000/vantage_points"
    
    if isinstance(vantage_points, list):
        vantage_points = ",".join(vantage_points)

    if ip_protocol is not None and 'ipv4' in ip_protocol and 'ipv6' in ip_protocol:
        ip_protocol = None

    # Prepare the parameters to send with the request
    params = {
        'ip_protocol': ip_protocol,
        'vantage_points': vantage_points,
    }
    
    try:
        # Send the request to the API
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the response as JSON if the request was successful
            return response.json()
        else:
            # Handle unsuccessful requests
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__": 
    r = get_vantage_points(ip_protocol=None, vantage_points='80.81.194.190,187.16.217.161,177.101.16.80,206.126.236.218,187.16.222.156')
    print (r)