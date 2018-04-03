# kalliope-web-scraper

A simple neuron for Kalliope to read part of web pages


## Synopsis

Make kalliope read information from any web page

## Installation

  ```
  kalliope install --git-url https://github.com/bacardi55/kalliope-web-scraper.git
  ```


## Options

| parameter                  | required | default | choices | comment                                                                                         |
|----------------------------|----------|---------|---------|-------------------------------------------------------------------------------------------------|
| url                        | yes      |         |         | The url of the site to parse                                                                    |
| main_selector_tag          | yes      |         |         | The main selector html tag that shoud return a list of htmlelement                              |
| main_selector_class        | yes      |         |         | The main selector class that shoud return a list of htmlelement                                 |
| title_selector_tag         | yes      |         |         | The selector html tag for the title in each element of the main_selector                        |
| title_selector_class       | yes      |         |         | The selector class for the title in each element of the main_selector                           |
| description_selector_tag   | yes      |         |         | The selector html tag for the description/summary/teaser/… in each element of the main_selector |
| description_selector_class | yes      |         |         | The selector class for the description/summary/teaser/… in each element of the main_selector    |


## Return Values

| Name         | Description                                                                           | Type     | sample   |
| ------------ | ------------------------------------------------------------------------------------- | -------- | -------- |
| returncode   | The http response code. If everything is ok, should be 200                            | string   |          |
| data         | List of item. Each news contains the title and content (new['title'] new['content']   | list     |          |


## Synapses example

This synapse will find read all "main" news on news.google.com
```
---
  - name: "Programme-tv"
    signals:
      - order: "What's on TV tonight"
    neurons:
      - web_scraper:
          url: "http://tvmag.lefigaro.fr/programme-tv/ce_soir_la_tv.html"
          main_selector_tag: "div"
          main_selector_class: "tvm-grid-channel__prog"
          title_selector_tag: "span"
          title_selector_class: "tvm-channel__logo"
          description_selector_tag: "h3"
          description_selector_class: "tvm-grid-channel__name"
          file_template: "templates/programme_tv.j2"
```

## Template example

```
{% if returncode != 200 %}
    Error while retrieving web page.
{% else %}
    {% for g in data: %}
        Title: {{ g['title'] }}
        Summary: {{ g['content'] }}
    {% endfor %}
{% endif %}
```



* [a blog about this neuron](http://bacardi55.org/2017/01/13/web-scrapping-kalliope-neuron.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)
