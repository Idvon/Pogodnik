def printing(data: dict) -> str:
    text = f"Weather in {data['city']}\n"\
           f"Country: {data['country']}\n"\
           f"State: {data['state']}\n"\
           f"Temperature: {data['temp']} \N{degree sign}C\n"\
           f"Humidity: {data['humidity']} %\n"\
           f"Wind speed: {data['windspd']} m/s\n"\
           f"Wind direction: {data['winddeg']}\N{degree sign}\n"\
           f"By {data['provider']}"
    return text
