# hue

## Synopsis

This neuron allow you to control your [Philips HUE](http://www2.meethue.com/en-us/about-hue/) lights from Kalliope.

## Installation

Install the neuron into your resource directory
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_hue.git
```

Before being able to use the neuron, you must establish an initial connection with your bridge in order to allow Kalliope to interact with it.
To do that, run the python script and follow instructions. This only needs to be run a single time.

You need to give the IP of your bridge as argument.  to discover the IP address of the bridge on your network. You can do this in a few ways:
1. Use a UPnP discovery app to find Philips hue in your network.
1. Log into your router and look Philips hue up in the DHCP table.
1. Via the Hue App into Network settings.

```bash
cd /path/to/your/resource_dir/neurons/hue
python bind_hue_bridge.py --ip <bridge_ip>
```
E.g:
```bash
cd /path/to/your/resource_dir/neurons/hue
python bind_hue_bridge.py --ip 192.168.0.7
```

## Options

You must set at least on of those parameters: `groups_name`, `lights_name`, `group_name`, `light_name`.

| parameter   | required | type    | default | choices | comment                                                |
|-------------|----------|---------|---------|---------|--------------------------------------------------------|
| bridge_ip   | YES      | string  |         |         | The IP address of your HUE bridge                      |
| groups_name | NO       | list    |         |         | List of group's name to switch                         |
| lights_name | NO       | list    |         |         | List of light's name to switch                         |
| group_name  | NO       | string  |         |         | Single group name to switch                            |
| light_name  | NO       | string  |         |         | Single light name to switch                            |
| state       | YES      | string  |         | on, off | Desired state of lights. Can be "on" or "off"          |
| brightness  | NO       | integer |         | 0-100   | Percentage of brightness of lamps in the target group. |

## Return Values

This neuron does not return any value

## Synapses example

Switch on all lights in the group called "hall" and "living-room"
```yml
 - name: "switch-on-bedroom"
   signals:
     - order: "turn the light on in the bedroom"
   neurons:
     - hue:
        bridge_ip: "192.168.0.7"
        groups_name:
         - "hall"
         - "living-room"
        state: "on"
```

Switch on a list of lights and set their brightness to the maximum level
```yml
 - name: "switch-on-bedroom"
   signals:
     - order: "turn the light on in the bedroom"
   neurons:
     - hue:
        bridge_ip: "192.168.0.7"
        lights_name:
         - "lamp1"
         - "lamp2"
        state: "on"
        brighness: 100
```

Use input parameter with bracket and a single group name in order control multiple lamps with the same synapse.
With the following synapse we can say:
- turn on the kitchen
- turn on the living room
- turn on the bedroom

```yml
- name: "turn-on"
  signals:
    - order: "turn on the {{ group_name }}"
  neurons:
    - hue:
        bridge_ip: "192.168.0.7"
        group_name:  "{{ group_name }}"
        state: "on"        
```

And the same synapse with state set to "off" can be used to turn off our lights.

## Notes

> **Note:** Your Kalliope installation must be placed on a device which is in the same network as the HUE bridge.

## Licence

MIT
