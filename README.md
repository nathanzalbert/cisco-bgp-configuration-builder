# Cisco BGP Configuration Builder

A Python tool that generates Cisco IOS BGP configurations from user input. The script simplifies BGP deployment by creating router, neighbor, and network statements without manually writing Cisco CLI commands.

## Features

* Configure a local BGP Autonomous System (AS)
* Set the BGP Router ID
* Add one or more BGP neighbors
* Configure neighbor descriptions
* Advertise multiple networks
* Export the generated configuration to a `.txt` file

## Requirements

* Python 3.x

## Usage

```bash
python bgp_builder.py
```

Follow the prompts to generate your Cisco BGP configuration.

## Example Output

```cisco
router bgp 65001
 bgp router-id 1.1.1.1
 bgp log-neighbor-changes
 neighbor 10.1.1.2 description Connection-to-R2
 neighbor 10.1.1.2 remote-as 65002
 network 192.168.10.0 mask 255.255.255.0
 network 192.168.20.0 mask 255.255.255.0
exit
```

## Skills Demonstrated

* Python
* Cisco IOS
* BGP Configuration
* Routing
* Network Automation
