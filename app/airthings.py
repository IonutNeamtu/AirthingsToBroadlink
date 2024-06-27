import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URL = 'https://accounts-api.airthings.com/v1/token'
AIRTHINGS_API_URL = 'https://ext-api.airthings.com/v1/devices/2960073452/latest-samples'


def get_access_token():
    try:
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, headers=headers, data=data,)
        # Check if response is successful
        response.raise_for_status()

        response_data = response.json()
        return response_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    except ValueError as ve:
        print(f"Failed to parse JSON response: {ve}")
        return None


def get_airthings_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(AIRTHINGS_API_URL, headers=headers)
    return response.json()


def process_sensor_data(data):
    temperature = data.get('temp')
    humidity = data.get('humidity')
    co2 = data.get('co2')
    voc = data.get('voc')
    pm25 = data.get('pm25')
    suggestions = []

    if temperature is not None and humidity is not None:
        if temperature > 28:
            print("Temperatura este ridicata.")
            suggestions.append("Temperatura este ridicata.")
        if 1000 > co2 > 800:
            print("Deschideti geamul, nivelul de co2 ridicat")
            suggestions.append("Deschideti geamul, nivelul de co2 ridicat")
        if co2 > 1000:
            print("Deschideti urgent geamul, nivelul de co2 este foarte ridicat")
            suggestions.append("Deschideti urgent geamul, nivelul de co2 este foarte ridicat")
        if humidity > 70:
            print("Nivel umiditate ridicat")
            suggestions.append("Nivel umiditate ridicat")
        if humidity < 30:
            print("Nivel umiditate scazut")
            suggestions.append("Nivel umiditate scazut")
        if pm25 > 10:
            print("Nivel pm2.5 ridicat")
            suggestions.append("Nivel pm2.5 ridicat")
        if voc > 250:
            print("Nivel voc ridicat")
            suggestions.append("Nivel voc ridicat")
    return suggestions
