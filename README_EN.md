<img src="./docs/pic.png" width="400px"/>

# PoGoDnIk
## Soft for pogoda
### Features:
___
#### - Weather for the selected city
#### - Output to console or web interface
#### - Output to database (Sqlite3)
#### - Output to CSV file
#### - Available providers:
##### [Open Weather](https://openweathermap.org)
##### [Open Meteo](https://open-meteo.com)

## Installation
___
### **Preparation**

Python 3.13 is recommended for running application

Instructions for Windows 10

Download repository
```
git clone https://github.com/Idvon/Pogodnik.git
```
### **Creating environment**

In CMD, navigate to repository directory and run the command
```commandline
virtualenv virtualenv_name
```
Activate environment
```commandline
virtualenv_name\Scripts\activate
```
Install packages
```
poetry install
```
### **Configure config file**

Supported formats

[Example JSON](example_config.json)

[Example TOML](example_config.toml)

Structure of config file

- `city_name`: Name of your city or a list of cities
- `timeout`: Cache duration for city weather in minutes
- `weather_provider`: Weather provider parameters 
  - `name`: Name
  - `api_key`: API key of the specified provider  
- `geo_provider`: Geolocation provider parameters   
  - `name`: Name  
  - `limit`: Number of displayed city search results (Only for web interface, default 5)  
  - `api_key`: API key of the specified provider

For Flask to work, the file must be named "config.json"

## **Run**  
___

Commands are entered in CMD within the activated environment

Output to console
```
python PoGoDnIk.py --config config.json --output out.csv
```
Sample output
```
Weather in Saint Petersburg
Country: RU
State: Saint Petersburg
Status: Clouds
Temperature: 3.41 °C
Humidity: 91 %
Wind speed: 5 m/s
Wind direction: SE
Clouds: 75 %
Precipitation: 0 mm
By openweather
```
Using the web interface
```
flask run
```
Located at: http://127.0.0.1:5000/

City input window:

<img src="./docs/welcome.png" width="400px"/>

Choosing a city from the list of found ones (from 1 to 5):

<img src="./docs/cities.png" width="400px"/>

Weather page (widget available from OpenWeather provider):

<img src="./docs/weather.png" width="400px"/>

### **Database**

Each relevant result is written to db.sqlite3 and the output file out.csv when timeout > time since the last request

Otherwise, data is retrieved from the database cache

## **Roadmap**
___

- [x] Alternative weather source
- [x] Database
- [x] Caching
- [x] Web interface
- [x] Output of weather forecast for the entire day, week (only OpenWeather)
- [ ] Docker container