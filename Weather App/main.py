import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io


def get_weather():
    city = city_entry.get()
    api_key = "https://v1.nocodeapi.com/youtoob/ow/ExjoeYmQysWtIjFf"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        display_weather(weather_data)
    else:
        messagebox.showerror("Error", "City not found!")


def display_weather(data):
    city_name = data['name']
    temp = data['main']['temp']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    
    weather_info = (
        f"City: {city_name}\n"
        f"Temperature: {temp}°C\n"
        f"Pressure: {pressure} hPa\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s\n"
        f"Description: {description.capitalize()}"
    )
    
    weather_label.config(text=weather_info)
    
    
    icon_code = data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    
    image_response = requests.get(icon_url)
    image_data = Image.open(io.BytesIO(image_response.content))
    image_data = image_data.resize((100, 100), Image.ANTIALIAS)
    
    weather_icon = ImageTk.PhotoImage(image_data)
    icon_label.config(image=weather_icon)
    icon_label.image = weather_icon  


root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")


city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=10)


get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=20)


weather_label = tk.Label(root, font=("Courier", 12), justify='left')
weather_label.pack(pady=10)


icon_label = tk.Label(root)
icon_label.pack(pady=10)


root.mainloop()