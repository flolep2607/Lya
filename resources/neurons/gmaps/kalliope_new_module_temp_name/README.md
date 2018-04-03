# kalliope-gmaps

A neuron to leverage googlemaps API

## Synopsis

Use GoogleMaps API to:

* Calculate distance between locations
* Get an address of a place based on a search
* Get directions to go between 2 locations with choice of mode (walking, driving, …)


To make it works, you will need to get an API key on your [developer console](https://console.developers.google.com/apis/dashboard).
Or follow [documentation here](https://developers.google.com/maps/documentation/distance-matrix/get-api-key)

The API that needs to be enabled are:

* [Google Places API Web Service](https://developers.google.com/places/web-service/)
* [Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/)
* [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/intro)

Depending on the action you will use, you might need just a subset of them (read below).

## Installation

  ```
  kalliope install --git-url https://github.com/bacardi55/kalliope-gmaps.git
  ```


## Options

| parameter     | required | default    | choices | comment                                                                                                 |
|---------------|----------|------------|---------|---------------------------------------------------------------------------------------------------------|
| gmaps_api_key | yes      |            | string  | The api key to use googlemaps API. See above.                                                           |
| origin    	| no       |            | string  | The address of the origin (departure address)                                                           |
| destination 	| no       |            | string  | The address of the destination (arrival address)                                                        |
| direction  	| no       | False      | Boolean | If you want the direction or just the distance/time                                                     |
| language   	| no       | en         | 0 or 1  | The language for the response                                                                           |
| units     	| no       | metric     |         | The [unit system](https://developers.google.com/maps/documentation/directions/intro#UnitSystems) to use |
| mode      	| no       | driving    |         | The [mode](https://developers.google.com/maps/documentation/directions/intro) to use                    |
| traffic_model | no       | best_guess |         | The [traffic_model](https://developers.google.com/maps/documentation/directions/intro) to use           |
| search     	| no       |            |         | The name of a place to search for via Gmaps API. Can be a place, a restaurant name , …                  | 


How to use:
* If ```search``` is set, will replace destination by an address return after a search on googlemaps of the named given in place (eg: "tour eiffel paris") *Requires Google Places API Web Service*
* If an origin is set, returns the distance between the origin and destination, the time needed to do the distance (with and without traffic estimation). *Requires Google Maps Distance Matrix API*
* If an origin is set and ```direction``` is set to ```True```, returns the same information than above (distance and time) but as well the steps to go from origin to destination. *Requires Google Maps Directions API*


## Return Values

| Name         | Description                                                                           | Type     | sample                            |
| ------------ | ------------------------------------------------------------------------------------- | -------- | --------------------------------- |
| status       |                                                                                       | String   | OK or KO                          |
| origin       | The given origin (so it can be reused in template)                                    | String   | 1 avenue des champs élysées Paris |
| destination  | The given destination address or the found address based on search name               | String   | 1 avenue des champs élysées Paris |
| search       | The name of the search place (so can be reused in template)                           | String   | Eiffel tour *or* restaurant xxx   |
| distance     | The distance between origin and destination                                           | String   | 9.1km                             |
| time         | The time to go from origin to destination                                             | String   | 19min                             |
| time_traffic | The time to go from origin to destination based on current traffic                    | String   | 20min                             |
| directions   | A list of steps to go from origin to destination                                      | List     | ["step 1", "step 2", … ]          |


## Synapses example

Get the distance and time between 2 locations

```yaml
  - name: "Gmaps-distance"
    signals:
      - order: "distance between {{origin}} and {{destination}}"
    neurons:
      - gmaps:
          gmaps_api_key: "*********"
          mode: "driving"
          language: "en"
          units: "metric"
          traffic_model: "pessimistic"
          origin: "{{origin}}"
          destination: "{{destination}}"
          file_template: "templates/en_gmaps.j2"
```

Get the distance between a defined place and a destination

```yaml
  - name: "Gmaps-distance-from-home"
    signals: 
      - order: "distance pour aller à {{destination}}"
    neurons:
      - gmaps:
          gmaps_api_key: "**************"
          mode: "driving"
          language: "en"
          units: "metric"
          origin: "***my home address***"
          mode: "driving"
          destination: "{{destination}}"
          file_template: "templates/en_gmaps.j2"
```

Get the address of a place by its name

```yaml
  - name: "Gmaps-place-address"
    signals: 
      - order: "get address of {{search}}"
    neurons:
      - gmaps:
          gmaps_api_key: "******************"
          language: "en"
          units: "metric"
          search: "{{search}}"
          file_template: "templates/en_gmaps.j2"
```

Get the direction to go to destination using the tube (if possible)

```yaml
  - name: "Gmaps-distance-from-home-by-tube"
    signals: 
      - order: "go by tube to {{destination}}"
    neurons:
      - gmaps:
          gmaps_api_key: "**************"
          mode: "transit"
          language: "en"
          units: "metric"
          origin: "**my home address"
          direction: True
          destination: "{{destination}}"
          file_template: "templates/en_gmaps.j2"
```

Get the direction to go to destination by car

```yaml
  - name: "Gmaps-directions-by-care"
    signals: 
      - order: "direction {{destination}}"
    neurons:
      - gmaps:
          gmaps_api_key: "**************"
          mode: "driving"
          language: "en"
          units: "metric"
          origin: "**my home address**"
          direction: True
          destination: "{{destination}}"
          file_template: "templates/en_gmaps.j2"
```

## Template example

#### English template

```
{% if status == "KO" %}
    Sorry, but the search didn't work, Sir
{% elif status == "OK" %}
    {% if search %}
        {% if origin %}
            Distance between {{ origin }} and {{ search }} is {{ distance }}.
            You need around {{time}} to go there
            {% if time_traffic %}
                You need to plan {{time_traffic}} with the current traffic
            {% endif %}
        {% else %}
            Address of {{search}} is {{destination}}
        {% endif %}
    {% elif destination %}
        Distance between {{oringi}} and {{destination}} is {{distance}}
        You need about {{ time }} to go there.
        {% if time_traffic %}
          Plan {{ time_traffic }} with current traffic.
        {% endif %}
    {% endif %}

    {% if directions %} 
        To go to {{destination}}, you need
        {% for direction in directions %}
            {{ direction }}
        {% endfor %}
    {% endif %}

{% endif %}
```

#### French template

```
{% if status == "KO" %}
    Désolé monsieur, mais une erreur est survenu lors du calcul.
{% elif status == "OK" %}
    {% if search %}
        {% if origin %}
	    La distance entre {{ origin }} et {{ search }} est de {{ distance }}. 
            Il faut environ {{ time }} pour y aller
            {% if time_traffic %}
                Il faut prévoir {{ time_traffic }} avec le traffic actuel.
            {% endif %}
        {% else %}
            L'addresse de {{ search }} est {{destination}}
        {% endif %}
    {% elif destination %}
        La distance entre {{ origin }} et {{ destination }} est de {{ distance }}. 
        Il faut environ {{ time }} pour y aller
        {% if time_traffic %}
          Il faut prévoir {{ time }} avec le traffic actuel.
        {% endif %}
    {% endif %}

    {% if directions %} 
        Pour se rendre à {{destination}}, il faut       :
        {% for direction in directions %}
            {{ direction }}
        {% endfor %}
    {% endif %}

{% endif %}
```


see more example in the [sample directory](https://github.com/bacardi55/kalliope-mpd/blob/master/samples/)

* [a post about this neuron](http://bacardi55.org/2017/02/21/kalliope-googlemaps-neuron.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)

