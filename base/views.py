
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

@api_view(['GET'])
def weather_forecast(request):
    city = request.GET.get('city')

    if not city:
        return Response({"error": "City is required"}, status=400)

    API_KEY = "d0c7aa0b055061c11773ee18409eeab8"

    try:
        # Step 1: Get latitude and longitude using Geocoding API
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            return Response({"error": "City not found"}, status=404)

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        city_name = geo_data[0]["name"]
        country = geo_data[0]["country"]

        # Step 2: Get weather using latitude and longitude
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)
        data = response.json()

        # DEBUG: print API response
        print(response.status_code)
        print(data)

        if response.status_code != 200:
            return Response(data, status=response.status_code)

        return Response({
            "city": city_name,
            "country": country,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"].title()
        })

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)
