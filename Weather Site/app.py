from flask import Flask, render_template, request
import requests


app = Flask(__name__)

API_KEY = '41fae3a5be3da3d37b2557a138d92861'  # OpenWeatherMap API Key
UNSPLASH_API_KEY = '2ltar3FgmqAlr-2quBeEIoAPHHaUcpWuJ5ZbloFXg30'  # Replace with your Unsplash API Access Key

@app.template_filter()
def format_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%A')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    image_url = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # Get geolocation data for the city
            location_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            location_response = requests.get(location_url)

            if location_response.status_code == 200:
                location_data = location_response.json()

                # Fetching image from Unsplash
                image_url_response = requests.get(f"https://api.unsplash.com/search/photos?query={city}&client_id={UNSPLASH_API_KEY}")
                if image_url_response.status_code == 200:
                    image_data = image_url_response.json()
                    if image_data['results']:
                        image_url = image_data['results'][0]['urls']['small']  # Get a small-sized image URL

                # Store the weather data
                weather_data = location_data
            else:
                error_message = "City not found!"

    return render_template('index.html', weather_data=weather_data, image_url=image_url, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)