# Google_agenda neuron for Kalliope

## Synopsis

Get your next meetings from your google agenda

## Installation

  ```
  kalliope install --git-url https://github.com/bacardi55/kalliope-google-calendar.git
  ```

## Options

| parameter          | required | default | choices | comment                                                                                                                         |
|--------------------|----------|---------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| credentials_file   | yes      |         |         | The json file downloaded on google calendar API, see the "Step 1: Turn on the Google Calendar API" of this page: https://developers.google.com/google-apps/calendar/quickstart/python                                              |
| client_secret_file | yes      |         |         | The file where the oauth credentials will be written                                                                            |
| application_name   | yes      |         |         | The name of your app as setup in google calendar api manager                                                                    |
| max_results        | yes      |         | integer | The number of event you want to retrieve                                                                                        |
| locale             | yes      |         |         | Your locale (eg: fr_FR.UTF-8). needs to be an installed locale on your system!                                                  |
| file_template      | yes      |         |         | Template file to use                                                                                                            |


## Return Values

| Name    | Description                   | Type   | sample                                                                                                                        |
|---------|-------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------|
| count   | The number of event retrieved | string | 3 (could be less than max_results if not enough event has been found)                                                         |
| events  | A list of events.             | list   | Each event has the following information: event['summary'], event['time']['weekday'], event['time']['day'], event['time']['month'], event['time']['hour'], event['time']['minute']                                  |


## Synapses example

```
---
  - name: "Google-agenda-next"
    signals:
      - order: "quels sont mes prochains rendez-vous"
    neurons:
      - google_calendar:
          credentials_file: "/path/to/credentials.json"
          client_secret_file: "/path/to/client_secret.json"
          scopes: "https://www.googleapis.com/auth/calendar.readonly"
          application_name: "App name"
          max_results: 3
          locale: fr_FR.UTF-8 # needs to be an installed locale
          no_meeting_msg: "You have no coming meetings"
          file_template: "templates/fr_google_calendar.j2"

```

Sample can be found in the [sample folder](samples).

## Templates example

```
{% if count > 0 %}
    Your next meetings are
    {% for event in events %}
        on {{ event['time']['weekday'] }}, {{ event['time']['day'] }}, {{ event['time']['month'] }}, à {{ event['time']['hour'] }} hour, {{ event['time']['minute'] }} :
        {{ event['summary'] }}
    {% endfor %}
{% else %}
    You don't have any meeting coming up
{% endif %}
```

Sample can be found in the [sample folder](samples).


* [Blog post about this neuron](http://bacardi55.org/2017/01/09/kalliope-neuron-for-google-calendar.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)
