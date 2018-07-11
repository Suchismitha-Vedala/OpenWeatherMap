OpenWeatherMap

This project is intended to get the weather of a city based on city id using Open Weather Map API and insert the data into MongoDB

The project is developed in python.
API configuration and list of city ids to be considered is written in config.py

Skills: Api Programming, Multithreading, Python, MongoDB

Command:
python program.py config.py


Process:
The program 
1.calls the Open Weather Map API 
2.Retrieves the data based on report type(5day/3 hr, 16day, weather_map, view map)
3.Inserts the data into Mongo DB
4.Opens the current weather map of the cities(with time stamp and temperature data) in a new window.
5.Prints Alert warnings if temperature is below 2degree Farenheit or it is Raining/Snowing in the Place
6.All the tasks are performed as threads in multithreaded programming.
