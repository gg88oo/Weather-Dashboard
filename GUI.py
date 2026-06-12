import tkinter as tk
import datetime
from project import weather_api

api = weather_api()

def get_deafult():
    try:
        with open("deafult.txt", "r") as file:
            city = file.read()
        return city
    except FileNotFoundError:
        return None

def set_deafult(city):
    with open("deafult.txt", "w") as file:
        file.write(city)

def get_weather_icon(condition):
    condition = condition.lower() if condition else ""
    if "clear" in condition or "sun" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "thunder" in condition:
        return "⛈️"
    else:
        return "🌡️"

def dispaly_weather(name):
    s = api.get_weather(name)
    if s != None:
        set_deafult(name)

        current_datetime = datetime.datetime.now()
        date_str = current_datetime.strftime("%d %B %Y")
        time_str = current_datetime.strftime("%H:%M")

        for widget in weather_frame.winfo_children():
            widget.destroy()

        datetime_frame = tk.Frame(weather_frame, bg='#f8f9ff')
        datetime_frame.pack(fill='x', padx=20, pady=20)

        date_info = tk.Frame(datetime_frame, bg='#f8f9ff')
        date_info.pack(side='left')

        date_day = current_datetime.strftime("%d")
        date_month = current_datetime.strftime("%B %Y")

        tk.Label(date_info, text=date_day, font=('Helvetica', 28, 'bold'), bg='#f8f9ff', fg='#2d3a5e').pack(anchor='w')
        tk.Label(date_info, text=date_month, font=('Helvetica', 16), bg='#f8f9ff', fg='#6b7a99').pack(anchor='w')

        time_info = tk.Frame(datetime_frame, bg='#f8f9ff')
        time_info.pack(side='right')

        tk.Label(time_info, text=time_str, font=('Helvetica', 36, 'bold'), bg='#f8f9ff', fg='#2d3a5e').pack(anchor='e')
        tk.Label(time_info, text="GMT +00:00", font=('Helvetica', 12), bg='#f8f9ff', fg='#6b7a99').pack(anchor='e')

        main_frame = tk.Frame(weather_frame, bg='white')
        main_frame.pack(fill='x', padx=30, pady=20)

        left_frame = tk.Frame(main_frame, bg='white')
        left_frame.pack(side='left')

        location_frame = tk.Frame(left_frame, bg='white')
        location_frame.pack(anchor='w')
        tk.Label(location_frame, text="📍", font=('Segoe UI Emoji', 24), bg='white').pack(side='left')
        tk.Label(location_frame, text=name.title(), font=('Helvetica', 32, 'bold'), bg='white', fg='#2d3a5e').pack(side='left', padx=10)

        temp_frame = tk.Frame(left_frame, bg='white')
        temp_frame.pack(anchor='w', pady=10)

        temp_value = str(s['temprature']).replace('°C', '').strip() if '°C' in str(s['temprature']) else str(s['temprature'])

        tk.Label(temp_frame, text=temp_value, font=('Helvetica', 72, 'bold'), bg='white', fg='#2d3a5e').pack(side='left')
        tk.Label(temp_frame, text="°C", font=('Helvetica', 32), bg='white', fg='#6b7a99').pack(side='left', anchor='s', pady=15)

        condition_frame = tk.Frame(left_frame, bg='white')
        condition_frame.pack(anchor='w')

        icon = get_weather_icon(s['weather'])
        tk.Label(condition_frame, text=icon, font=('Segoe UI Emoji', 48), bg='white').pack(side='left')
        tk.Label(condition_frame, text=s['weather'], font=('Helvetica', 20), bg='white', fg='#6b7a99').pack(side='left', padx=10)

        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side='right')

        tk.Label(right_frame, text=icon, font=('Segoe UI Emoji', 100), bg='white').pack()

        details_frame = tk.Frame(weather_frame, bg='white')
        details_frame.pack(fill='x', padx=30, pady=20)

        details_grid = tk.Frame(details_frame, bg='white')
        details_grid.pack()

        for i, (key, config) in enumerate(detail_items.items()):
            frame = tk.Frame(details_grid, bg='#f8f9ff', width=150, height=100)
            frame.grid(row=i//3, column=i%3, padx=8, pady=8)
            frame.pack_propagate(False)

            inner = tk.Frame(frame, bg='#f8f9ff')
            inner.pack(expand=True)

            tk.Label(inner, text=config['icon'], font=('Segoe UI Emoji', 24), bg='#f8f9ff').pack()
            tk.Label(inner, text=config['label'], font=('Helvetica', 10), bg='#f8f9ff', fg='#6b7a99').pack()

            if key in s:
                value = s[key]
            elif key == 'humidity':
                value = '65%'
            elif key == 'uv':
                value = '4'
            elif key == 'sunrise':
                value = '06:32'
            elif key == 'sunset':
                value = '19:45'
            elif key == 'visibility':
                value = '10 km'
            else:
                value = '--'

            tk.Label(inner, text=str(value), font=('Helvetica', 14, 'bold'), bg='#f8f9ff', fg='#2d3a5e').pack()
            tk.Label(inner, text=config['sub'], font=('Helvetica', 9), bg='#f8f9ff', fg='#6b7a99').pack()

        badge_frame = tk.Frame(weather_frame, bg='white')
        badge_frame.pack(pady=(0, 20))

        badge = tk.Frame(badge_frame, bg='#f8f9ff', bd=1, relief='solid', highlightbackground='#eef0f5')
        badge.pack()

        dot = tk.Frame(badge, bg='#ffb347' if s['is_day'] == 'Day' else '#6b7a99', width=10, height=10)
        dot.pack(side='left', padx=10, pady=8)
        dot.pack_propagate(False)

        tk.Label(badge, text=f"{s['is_day']} Mode", font=('Helvetica', 12, 'bold'), bg='#f8f9ff', fg='#2d3a5e').pack(side='left')

    else:
        display_label.config(text="Having trouble finding this location")

def req_weth():
    if entry_label.get():
        dispaly_weather(entry_label.get())

def refresh():
    city = get_deafult()
    if city:
        entry_label.delete(0, tk.END)
        entry_label.insert(0, city)
        dispaly_weather(city)

window = tk.Tk()
window.title("Weather")
window.geometry("700x900")
window.configure(bg='#667eea')

main_container = tk.Frame(window, bg='white', bd=0, highlightthickness=0)
main_container.pack(padx=20, pady=20, fill='both', expand=True)

header_frame = tk.Frame(main_container, bg='#6b8cff', highlightthickness=0)
header_frame.pack(fill='x', padx=0, pady=0)

tk.Label(header_frame, text="⛅", font=('Segoe UI Emoji', 28), bg='#6b8cff', fg='white').pack(side='left', padx=(20,10), pady=20)
tk.Label(header_frame, text="Weather Dashboard", font=('Helvetica', 24, 'bold'), bg='#6b8cff', fg='white').pack(side='left', pady=20)

search_frame = tk.Frame(header_frame, bg='#6b8cff')
search_frame.pack(fill='x', padx=20, pady=(0,20))

entry_label = tk.Entry(search_frame, font=('Helvetica', 14), bg='#2d3a5e', fg='white', bd=0, insertbackground='white')
entry_label.pack(side='left', fill='x', expand=True, ipady=12)
entry_label.insert(0, "Enter city name...")

search_btn = tk.Button(search_frame, text="🔍 Search", font=('Helvetica', 12, 'bold'), bg='white', fg='#6b8cff', bd=0, padx=20, cursor='hand2', command=req_weth)
search_btn.pack(side='left', padx=10)

refresh_btn = tk.Button(search_frame, text="↻ Refresh", font=('Helvetica', 12), bg='#2d3a5e', fg='white', bd=0, padx=20, cursor='hand2', command=refresh)
refresh_btn.pack(side='left')

weather_frame = tk.Frame(main_container, bg='white', highlightthickness=0)
weather_frame.pack(fill='both', expand=True, padx=0, pady=0)

display_label = tk.Label(master=window, text="", bg='#667eea')
display_label.pack()

detail_items = {
    'windspeed': {'icon': '💨', 'label': 'WIND SPEED', 'sub': 'Gentle breeze'},
    'humidity': {'icon': '💧', 'label': 'HUMIDITY', 'sub': 'Moderate'},
    'uv': {'icon': '☀️', 'label': 'UV INDEX', 'sub': 'Moderate'},
    'sunrise': {'icon': '🌅', 'label': 'SUNRISE', 'sub': '1 hour ago'},
    'sunset': {'icon': '🌇', 'label': 'SUNSET', 'sub': 'in 5 hours'},
    'visibility': {'icon': '👁️', 'label': 'VISIBILITY', 'sub': 'Clear'}
}

if get_deafult() != None:
    entry_label.delete(0, tk.END)
    entry_label.insert(0, get_deafult())
    dispaly_weather(get_deafult())

window.mainloop()
