import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime
import threading

def get_weather():
    api_key = '4f6b3b54850ed3da4024173360334f49'
    city = city_var.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        icon_code = data['weather'][0]['icon']
        
        # Update GUI with weather data
        weather_label.config(text=f"Cuaca: {weather}")
        temp_label.config(text=f"Suhu: {temperature}°C, Terasa Seperti: {feels_like}°C")
        humidity_label.config(text=f"Kelembapan: {humidity}%")
        wind_label.config(text=f"Kecepatan Angin: {wind_speed} m/s")
        pressure_label.config(text=f"Tekanan Udara: {pressure} hPa")
        last_update_label.config(text=f"Terakhir diperbarui: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Get and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_response.raise_for_status()
        icon_data = icon_response.content
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Tidak dapat mengambil data cuaca: {e}")
        weather_label.config(text="Error: Tidak dapat mengambil data cuaca.")
        temp_label.config(text="")
        humidity_label.config(text="")
        wind_label.config(text="")
        pressure_label.config(text="")
        icon_label.config(image='')

    # Stop loading animation
    loading_label.pack_forget()

def get_forecast():
    api_key = '4f6b3b54850ed3da4024173360334f49'
    city = city_var.get()
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        forecast_data = []
        for forecast in data['list']:
            dt = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = forecast['main']['temp']
            weather = forecast['weather'][0]['description'].capitalize()
            forecast_data.append((dt, temp, weather))
        
        # Display forecast data in a new window
        forecast_window = tk.Toplevel(root)
        forecast_window.title("Prakiraan Cuaca 5 Hari")
        
        tree = ttk.Treeview(forecast_window, columns=('Tanggal', 'Suhu', 'Cuaca'), show='headings')
        tree.heading('Tanggal', text='Tanggal')
        tree.heading('Suhu', text='Suhu (°C)')
        tree.heading('Cuaca', text='Cuaca')
        
        for item in forecast_data:
            tree.insert('', 'end', values=item)
        
        tree.pack(fill=tk.BOTH, expand=True)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Tidak dapat mengambil data prakiraan cuaca: {e}")

def refresh_weather():
    # Start loading animation
    loading_label.pack(pady=10)
    threading.Thread(target=get_weather).start()

# Set up the main application window
root = tk.Tk()
root.title("Aplikasi Prakiraan Cuaca")
root.geometry("800x600")

# Apply theme
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12))

# Create a frame for the weather info
frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# List of cities in Indonesia
cities = [
    'Semarang', 'Jakarta', 'Surabaya', 'Bandung', 'Yogyakarta', 'Medan', 'Palembang', 'Makassar', 'Denpasar', 'Balikpapan',
    'Pekanbaru', 'Batam', 'Padang', 'Malang', 'Samarinda', 'Tasikmalaya', 'Pontianak', 'Banjarmasin', 'Manado', 'Kupang'
]

# Create dropdown to select city
city_var = tk.StringVar()
city_combobox = ttk.Combobox(frame, textvariable=city_var, values=cities)
city_combobox.pack(pady=10)
city_combobox.set('Semarang')

# Create labels to display the weather data
weather_label = ttk.Label(frame, text="Cuaca: Memuat...", font=('Helvetica', 16))
weather_label.pack(pady=10)

temp_label = ttk.Label(frame, text="Suhu: Memuat...", font=('Helvetica', 16))
temp_label.pack(pady=10)

humidity_label = ttk.Label(frame, text="Kelembapan: Memuat...", font=('Helvetica', 16))
humidity_label.pack(pady=10)

wind_label = ttk.Label(frame, text="Kecepatan Angin: Memuat...", font=('Helvetica', 16))
wind_label.pack(pady=10)

pressure_label = ttk.Label(frame, text="Tekanan Udara: Memuat...", font=('Helvetica', 16))
pressure_label.pack(pady=10)

last_update_label = ttk.Label(frame, text="Terakhir diperbarui: Memuat...", font=('Helvetica', 12))
last_update_label.pack(pady=10)

# Create label for weather icon
icon_label = ttk.Label(frame)
icon_label.pack(pady=10)

# Loading animation label
loading_label = ttk.Label(frame, text="Memuat...", font=('Helvetica', 12))

# Button to refresh weather data
refresh_button = ttk.Button(frame, text="Refresh Cuaca", command=refresh_weather)
refresh_button.pack(pady=20)

# Button to get forecast data
forecast_button = ttk.Button(frame, text="Prakiraan Cuaca 5 Hari", command=get_forecast)
forecast_button.pack(pady=10)

# Initial weather data fetch
refresh_weather()

# Start the main event loop
root.mainloop()
