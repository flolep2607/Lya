# kalliope-wwtime

A neuron to ask time in a specific country

## Synopsis

This neuron will retrieve a local timezone and a requested city timezone. It compares timezone difference (including summer time) between the two location to give you the time there based on your timezone.

Eg:

- I am in Paris (GMT +1)
- I want to know Boston time (GMT -5 - and as of now - summer time (so 1 additional hour))

When it's 10pm in Paris, Kalliope will tell me it is 5pm in Boston (because as of now, boston is in summer time and paris not yet, so -5 and not -6)


It uses GoogleMaps API to get geolocation data based on a city name or address. So you need to activate to Google API:

- [Google Maps Time Zone API](https://developers.google.com/maps/documentation/timezone/intro)
- [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro)


To make it works, you will need to get an API key on your [developer console](https://console.developers.google.com/apis/dashboard).
Or follow [documentation here](https://developers.google.com/maps/documentation/geocoding/get-api-key) and [here](https://developers.google.com/maps/documentation/timezone/get-api-key)

## Installation

```
kalliope install --git-url https://github.com/bacardi55/kalliope-wwtime.git
```


## Options

| parameter     | required | default    | choices | comment                                                                                                 |
|---------------|----------|------------|---------|---------------------------------------------------------------------------------------------------------|
| gmaps_api_key | yes      |            | string  | The api key to use googlemaps API. See above.                                                           |
| local         | yes      |            | string  | Your city/address to compare time difference with                                                       |
| city          | yes      |            | string  | What city/address where you want to know time                                                           |



## Return Values

| Name    | Description                         | Type     | sample                            |
| --------| ----------------------------------- | -------- | --------------------------------- |
| status  | Response status                     | String   | OK or KO                          |
| city    | A dict¹ (see below)                 | dict     | [arg: 'new york city', 'timezoneid': 'America/New_York', 'timezonename': 'Eastern Daylight Time', time: {'hour': '10', 'minute': '30'}] |
| local   | A dict¹ (see below)                 | dict     | [arg: 'Paris France', 'timezoneid': 'Europe/Paris', 'timezonename': 'Central European Standard Time', time: {'hour': '10', 'minute': '30'}] |

¹: these dict contains:

- arg: The given name in arguments (equals 'local' argument for local return variable or 'city' arguments for city return variable)
- timezoneid: The ID of the timezone, eg: Europe/Paris
- timezonename: The name of the timezone eg: Central European Standard Time
- time, a dict containing 'hour' and 'minutes'

## Synapses example

### brains

Get a city by argument in order

```yaml
  - name: "Wwtime-city"
    signals:
      - order: "Give me the time in {{city}}"
    neurons:
      - wwtime:
          gmaps_api_key: "GMAPS_API_KEY"
          local: "Paris France"
          city: "{{city}}"
          file_template: "templates/fr_wwtime.j2"
```

Get a city by argument set in brain:

```yaml
  - name: "Wwtime-city-boton"
    signals:
      - order: "time in boston"
    neurons:
      - wwtime:
          gmaps_api_key: "GMAPS_API_KEY"
          city: "boston MA"
          local: "Paris France"
          file_template: "templates/fr_wwtime.j2"
```

### template

```jinja
{% if status == "OK" %}
    Sir, in {{city.arg}}, it is {{city.time.hour}} hour and {{city.time.minute}} minutes, whereas here, it's {{local.time.hour}} hour and {{local.time.minute}} minutes
    Le timezone est {{city.timezonename}}
{% else %}
    Sorry sir, but I don't know
{% endif %}
```

see more example in the [sample directory](https://github.com/bacardi55/kalliope-wwtime/blob/master/samples/)


* [my posts about kalliope](http://bacardi55.org/kalliope.html)

