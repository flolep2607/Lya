# kalliope-uber

A neuron to leverage Uber API

## Synopsis

Use Uber API to:

* Get the time needed for a driver to arrive at your starting address
* Get the price and duration of a ride from starting address to end address

You need to enable [uber API](https://developer.uber.com/dashboard) for this. More information [here](https://developer.uber.com/docs/riders/introduction).

This neuron only leverage the server token and not a end user oauth2 connection per user.

This is due to the limited use case available by this neuron. User **can't** book a ride from this neuron. I don't intend to develop this as I don't want to automate Uber reservation (i found it a bit dangerous imo :)). But if anyone want ot add it, i'm happy to look at pull requests :).


## Installation

```
kalliope install --git-url https://github.com/bacardi55/kalliope-uber.git
```

This will install [uber-riders](https://github.com/uber/rides-python-sdk) python library **and** [google maps python lib](https://github.com/googlemaps/google-maps-services-python). The google maps API is only needed to transform address into geolocation data (longitude/latitude). If you provide longitude / latitude data instead of address, gmaps lib won't get loaded and won't be used. Please read next section for more information

## Options

| parameter       | required | default | choices | comment                                                              |
|-----------------|----------|---------|---------|----------------------------------------------------------------------|
| uber_api_key    | yes      |         | string  | The api key to use uber API. See below.                              |
| gmaps_api_key   | no       |         | string  | The api key to use googlemaps API. See below.                        |
| drive_mode	  | yes      | uberX   | string  | The drive mode: uberX, uberBlack, pool', ... [Complete list here](https://developer.uber.com/docs/riders/references/api/v1.2/products-get)  |
| start_latitude  | no       |         | string  | The latitude of the start / origin address                           |
| start_longitude | no       |         | string  | The longitude of the start / origin address                          |
| start_address   | no       |         | string  | The full text start / origin address                                 |
| end_latitude    | no       |         | string  | The latitude of the destination address                              |
| end_longitude   | no       |         | string  | The longitude of the destination address                             |
| end_address     | no       |         | string  | The full text destination address                                    |


**Additional notes**:

* If start_address is given, Gmaps will be used to get geolocation data and will replace the given start_{longitude,latitude} if any
* If end_address is given, Gmaps will be used to get geolocation data and will replace the given end_{longitude,latitude} if any
* If either start_address or end_address is given, gmaps_api_key is mandatory.
* If you want to use the gmaps geolocation api, you need to enable the [Google Maps geolocation API](https://developers.google.com/maps/documentation/geocoding/intro)


## Return Values

TODO: review arguments sample and description 

| Name               | Description                                                                           | Type     | sample                            |
|--------------------|---------------------------------------------------------------------------------------|----------|-----------------------------------|
| driving_mode       | The driving method (= drive_mode) arguments                                           | String   | ubserX, pool                      |
| time_to_get_driver | The time to get a driver                                                              | String   | 3 minutes                         |
| distance           | The distance between start and end addresses. Only if end_address is provided         | String   | 11.3 km                           |
| high_estimate      | The high estimate price for the ride. Only given if end_address is provided           | String   | 13                                |
| low_estimate       | The low estimate price for the ride. Only given if end_address is provided            | String   | 10                                |
| duration           | The time to go from origin to destination. Only given if end_address is provided      | String   | 19 min                            |
| estimate           | The average time estimate to go from start to end address                             | String   | $20                               |


## Synapses example

Get the estimated time to get a ```driving_mode``` driver based on geolocation data

```yaml
  - name: "Uber-time-estimate"
    signals:
      - order: "how long for a driver to pick me up"
    neurons:
      - say:
          message: "Calculating"
      - uber:
          uber_api_key: "***********************"
          start_longitude: "***"
          start_latitude: "****"
          driving_mode: "uberX"
          say_template: "A {{driving_mode}} driver can be there in {{ time_to_get_driver }} minutes"
```

Get the estimated time to get a ```driving_mode``` based on a text address

```yaml
  - name: "Uber-time-estimate-by-address"
    signals:
      - order: "how long for a driver to pick me up"
    neurons:
      - say:
          message: "Calculating"
      - uber:
          uber_api_key: "***********************"
          gmaps_api_key: "**********************"
          start_address: "*********"
          driving_mode: "uberX"
          say_template: "A {{driving_mode}} driver can be there in {{ time_to_get_driver }} minutes"
```

Get the estimated time to get a ```driving_mode```, the price and the ride duration

```yaml
  - name: "Uber-time-and-price"
    signals:
      - order: "how much for a rider to work"
    neurons:
      - say:
          message: "Calculating"
      - uber:
          uber_api_key: "***********************"
          driving_mode: "uberX"
          start_longitude: "***"
          start_latitude: "****"
          end_longitude: "*****"
          end_latitude: "******"
          say_template: "A {{driving_mode}} driver can be there in {{ time_to_get_driver }} minutes. Traject will take about {{ duration }} and would cost {{ estimate }}"
```
 
Get the estimated time to get a ```driving_mode```, the price and the ride duration to go to an address givin in argument

```yaml
  - name: "Uber-time-and-price-by-addresses"
    signals:
      - order: "how much for a rider to {{end_address}}"
    neurons:
      - say:
          message: "Calculating"
      - uber:
          uber_api_key: "***********************"
          gmaps_api_key: "**********************"
          start_address: "*********"
          driving_mode: "uberX"
          say_template: "A {{driving_mode}} driver can be there in {{ time_to_get_driver }} minutes. Traject will take about {{ duration }} and would cost {{ estimate }}"
          end_address: "{{end_address}}"

```

Get the estimated time to get a ```driving_mode```, the price and the ride duration based on addresses given in arguments

```yaml
  - name: "Uber-time-and-price-by-start-address"
    signals:
      - order: "how long for a driver to pick me up {{start_address}} to go to {{end_address}}"
    neurons:
      - say:
          message: "Calculating"
      - uber:
          uber_api_key: "***********************"
          gmaps_api_key: "**********************"
          driving_mode: "uberX"
          say_template: "A {{driving_mode}} driver can be there in {{ time_to_get_driver }} minutes. Traject will take about {{ duration }} and would cost {{ estimate }}"
          start_address: "{{start_address}}"
          end_address: "{{end_address}}"
```


see more example in the [sample directory](https://github.com/bacardi55/kalliope-uber/blob/master/samples/)


* [my posts about kalliope](http://bacardi55.org/en/term/kalliope)

