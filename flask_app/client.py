import requests


# Client class to search for city names
# API: https://rapidapi.com/wirefreethought/api/geodb-cities
# Endpoints Used: Cities
class CityClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        self.headers = {
            "X-RapidAPI-Key": "a348e39a40msh5aebd50a33e7f0dp185d1ejsnd63a0c5dd1f2",
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
        }

    # Search for cities whose name has the string provided in query as a prefix
    def search_cities(self, query):
        params = {
            "types": "city",
            "distanceUnit": "mi",
            "languageCode": "en",
            "sort": "-population",
            "namePrefix": query,
        }
        response = requests.get(self.url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise ValueError("Search request failed. Please try again later.")

        data = response.json()
        return data["data"]


# Client class to grab weather data
# API: https://rapidapi.com/weatherapi/api/weatherapi-com
# Endpoints Used: Forecast Weather API, History Weather API
class WeatherClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.forecast_url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        self.history_url = "https://weatherapi-com.p.rapidapi.com/history.json"
        self.headers = {
            "X-RapidAPI-Key": "a348e39a40msh5aebd50a33e7f0dp185d1ejsnd63a0c5dd1f2",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        }

    # Gets current realtime forecast for the provided location
    def get_forecast(self, location):
        params = {"q": location, "days": "3"}
        response = requests.get(self.forecast_url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise ValueError("Forecast retrieval failed. Please try again later.")

        return response.json()

    # Gets forecast history for the provided location.
    # Grabs the forecast starting on the provided starting_date and ending on the
    # provided ending_date.
    def get_history(self, location, starting_date, ending_date):
        params = {"q": location, "dt": starting_date, "end_dt": ending_date}
        response = requests.get(self.history_url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise ValueError(
                "Forecast History retrieval failed. Please try again later."
            )

        return response.json()
