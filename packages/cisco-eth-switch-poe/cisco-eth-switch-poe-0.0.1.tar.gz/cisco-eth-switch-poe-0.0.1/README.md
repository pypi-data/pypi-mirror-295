# README

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for?

- This repository is a part of opsys automation infrastructure
- This repository is Cisco ETH switch 220 controller implementation for POE management

### How do I get set up?

- pip install cisco-eth-switch-poe

### Unit Testing

- python -m unittest -v

### References
```
https://www.cisco.com/c/en/us/td/docs/switches/lan/csbss/CBS220/CLI-Guide/b_220CLI/power_over_ethernet_poe_commands.html#ID-000037a8
```

### Telnet Configuration
```
1. Log-In to Cisco switch web-UI.
2. Go to Security -> TCP/UDP Services.
3. Check "Telnet" checkbox and press "Apply" button.
4. Connect via CLI to Telnet with user and password configured in web-UI.
```

### Usage Example

```
from cisco_eth_switch_poe.cisco_eth_switch_poe import CiscoEthSwitchPoe

switch = CiscoEthSwitchPoe(username='user',
                           password='pass',
                           ip_address='10.0.0.2',
                           telnet_port=23,
                           timeout=2)

switch.connect()
print(switch.show_power_inline())
switch.disconnect()
```
