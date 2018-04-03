# kalliope-system-status

A neuron for Kalliope to tell you system data


Shamelessly inspired from https://github.com/edouardpoitras/jasper-status


## Synopsis

Let Kalliope tell you its status

## Installation

  ```
  kalliope install --git-url https://github.com/bacardi55/kalliope-system-status.git
  ```


## Options

| parameter  | required | default   | choices | comment                                                                                    |
|------------|----------|-----------|---------|--------------------------------------------------------------------------------------------|

No option so far


## Return Values

| Name           | Description                                                                           | Type     | sample      |
| -------------- | ------------------------------------------------------------------------------------- | -------- | --------    |
| running_since  |                                                                                       |          |             |
| os             | OS name                                                                               | String   | Linux       |
| os_version     | Kernel version                                                                        | String   | 4.4.2       |
| system_name    | Name of your host                                                                     | String   | raspberrypi |
| system_nb_core | Number of core                                                                        | String   | 4           |
| cpu            | % of CPU usage                                                                        | String   | 10.4        |
| memory         | % of memory usage                                                                     | String   | 32.1        |
| disk           | % of disk usage                                                                       | String   | 11.5        |


## Synapses example

```yaml
---
  - name: "System-status"
    signals:
      - order: "Step into analysis mode, please"
    neurons:
      - system_status:
          say_template: 
            - "I'm running on {{os}}, kernel {{os_version}}, with {{system_nb_cores}} cores.    C P U usage {{cpu}} %  memory usage {{memory}} %  disk usage {{disk}} %"
          cache: False
```

## Template example



* [a blog post about this neuron](http://bacardi55.org/2017/02/21/kalliope-system-status-neuron.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)

