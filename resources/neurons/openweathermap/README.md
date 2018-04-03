# OpenWeatherMap API

## Synopsis 

Give the today and tomorrow weather with the related data (humidity, temperature, etc ...) for a given location. 

## Installation
```
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_openweathermap.git
```

## Options

| parameter | required | default | choices                     | comment                                                                                           |
|-----------|----------|---------|-----------------------------|---------------------------------------------------------------------------------------------------|
| api_key   | YES      | None    |                             | User API key of the OWM API                                                                       |
| location  | YES      | None    |                             | The location                                                                                      |
| lang      | No       | en      | multiple                    | First 2 letters cf : section Multilingual support in : [lang](https://openweathermap.org/current) |
| temp_unit | No       | Kelvin  | Celsius, Kelvin, Fahrenheit |                                                                                                   |
| country   | No       | US      | multiple                    |  Frist 2 letters of the country cf API doc                                                        |

## Return Values

| Name                        | Description                                | Type   | sample                 |
|-----------------------------|--------------------------------------------|--------|------------------------|
| location                    | The current location                       | String | Grenoble               |
| weather_today               | Today : The weather sentence               | String | cloudy                 |
| sunset_today_time           | Today : The sunset time (iso)              | String | 2016-10-15 20:07:57+00 |
| sunrise_today_time          | Today : The sunrise time (iso)             | String | 2016-10-15 07:07:57+00 |
| temp_today_temp             | Today : Average temperature                | float  | 25                     |
| temp_today_temp_max         | Today : Max temperature                    | float  | 45                     |
| temp_today_temp_min         | Today : Min temperatue                     | float  | 5                      |
| pressure_today_press        | Today : Pressure                           | float  | 1009                   |
| pressure_today_sea_level    | Today : Pressure at the Sea level          | float  | 1038.381               |
| humidity_today              | Today : % of humidity                      | float  | 60                     |
| wind_today_deg              | Today : Direction of the wind in degree    | float  | 45                     |
| wind_today_speed            | Today : Wind speed                         | float  | 2.66                   |
| snow_today                  | Today : Volume of snow                     | float  | 0                      |
| rain_today                  | Today : Rain volume                        | float  | 0                      |
| clouds_coverage_today       | Today : % Cloud coverage                   | float  | 65                     |
| weather_tomorrow            | Tomorrow : The weather sentence            | String | sunny                  |
| sunset_time_tomorrow        | Tomorrow : The sunset time (iso)           | String | 2016-10-16 20:07:57+00 |
| sunrise_time_tomorrow       | Tomorrow : The sunrise time (iso)          | String | 2016-10-16 07:07:57+00 |
| temp_tomorrow_temp          | Tomorrow : Average temperature             | float  | 25                     |
| temp_tomorrow_temp_max      | Tomorrow : Max temperature                 | float  | 45                     |
| temp_tomorrow_temp_min      | Tomorrow : Min temperatue                  | float  | 5                      |
| pressure_tomorrow_press     | Tomorrow : Pressure                        | float  | 1009                   |
| pressure_tomorrow_sea_level | Tomorrow : Pressure at the Sea level       | float  | 1038.381               |
| humidity_tomorrow           | Tomorrow : % of humidity                   | float  | 60                     |
| wind_tomorrow_deg           | Tomorrow : Direction of the wind in degree | float  | 45                     |
| wind_tomorrow_speed         | Tomorrow : Wind speed                      | float  | 2.66                   |
| snow_tomorrow               | Tomorrow : Volume of snow                  | float  | 0                      |
| rain_tomorrow               | Tomorrow : Rain volume                     | float  | 0                      |
| clouds_coverage_tomorrow    | Tomorrow : % Cloud coverage                | float  | 65                     |

## Synapses example


```
  - name: "get-the-weather"
    signals:
      - order: "quel temps fait-il"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "fr"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template:
          - "Aujourd'hui a {{ location }} le temps est {{ weather_today }} avec une température de {{ temp_today_temp }} degrés et demain le temps sera {{ weather_tomorrow }} avec une température de {{ temp_tomorrow_temp }} degrés"
```
Load the location from your order
```
  - name: "getthe-weather"
    signals:
      - order: "what is the weather in {{ location }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location: "{{ location }}"
          say_template:
          - "Today in {{ location }} the weather is {{ weather_today }} with a temperature of {{ temp_today_temp }} degree and tomorrow the weather will be {{ weather_tomorrow }} with a temperature of {{ temp_tomorrow_temp }} degree"
          
```

## Templates example 

```
Today in {{ location }} the weather is {{ weather_today }} with a temperature of {{ temp_today_temp }} degree
```


## Notes

> **Note:** You need to create a free account on [openweathermap.org](http://openweathermap.org/) to get your API key.

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
