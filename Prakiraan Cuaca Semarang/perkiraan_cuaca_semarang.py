import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def get_weather():
    api_key = '4f6b3b54850ed3da4024173360334f49'
    city = 'Semarang'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        icon_code = data['weather'][0]['icon']
        
        # Update GUI with weather data
        weather_label.config(text=f"Cuaca: {weather}")
        temp_label.config(text=f"Suhu: {temperature}°C, Terasa Seperti: {feels_like}°C")
        humidity_label.config(text=f"Kelembapan: {humidity}%")

        # Get and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = icon_response.content
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
    else:
        weather_label.config(text="Error: Tidak dapat mengambil data cuaca.")
        temp_label.config(text="")
        humidity_label.config(text="")
        icon_label.config(image='')

# Set up the main application window
root = tk.Tk()
root.title("Aplikasi Prakiraan Cuaca Semarang")

# Create a frame for the weather info
frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# Create labels to display the weather data
weather_label = ttk.Label(frame, text="Cuaca: Memuat...", font=('Helvetica', 16))
weather_label.pack(pady=10)

temp_label = ttk.Label(frame, text="Suhu: Memuat...", font=('Helvetica', 16))
temp_label.pack(pady=10)

humidity_label = ttk.Label(frame, text="Kelembapan: Memuat...", font=('Helvetica', 16))
humidity_label.pack(pady=10)

# Create label for weather icon
icon_label = ttk.Label(frame)
icon_label.pack(pady=10)

# Button to refresh weather data
refresh_button = ttk.Button(frame, text="Refresh Cuaca", command=get_weather)
refresh_button.pack(pady=20)

# Initial weather load
get_weather()

# Start the GUI event loop
root.mainloop()
