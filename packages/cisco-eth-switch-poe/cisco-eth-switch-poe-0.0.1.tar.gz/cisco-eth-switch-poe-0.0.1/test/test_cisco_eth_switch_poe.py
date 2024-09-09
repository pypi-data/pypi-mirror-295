import unittest
from unittest.mock import patch, MagicMock
from cisco_eth_switch_poe.cisco_eth_switch_poe import CiscoEthSwitchPoe


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(CiscoEthSwitchPoe, 'switch_login')
    def test_switch_login(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.switch_login()
        relay_mock.assert_called_once_with()
        
    @ patch.object(CiscoEthSwitchPoe, 'connect')
    def test_connect(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.connect()
        relay_mock.assert_called_once_with()

    @ patch.object(CiscoEthSwitchPoe, 'disconnect')
    def test_connect(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.disconnect()
        relay_mock.assert_called_once_with()
        
    @ patch.object(CiscoEthSwitchPoe, 'enter_config_mode')
    def test_enter_config_mode(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.enter_config_mode()
        relay_mock.assert_called_once_with()
        
    @ patch.object(CiscoEthSwitchPoe, 'enter_interface_config')
    def test_enter_interface_config(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.enter_interface_config()
        relay_mock.assert_called_once_with()
    
    @ patch.object(CiscoEthSwitchPoe, 'exit_config_mode')
    def test_exit_config_mode(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        relay_conn.exit_config_mode()
        relay_mock.assert_called_once_with()
        
    @ patch.object(CiscoEthSwitchPoe, 'show_power_inline')
    def test_show_power_inline(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        first_interface = 1
        last_interface = 3
        relay_conn.show_power_inline(first_interface=first_interface, last_interface=last_interface)
        relay_mock.assert_called_once_with(first_interface=1, last_interface=3)
    
    @ patch.object(CiscoEthSwitchPoe, 'show_power_inline_consumption')
    def test_show_power_inline_consumption(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        first_interface = 1
        last_interface = 3
        relay_conn.show_power_inline_consumption(first_interface=first_interface, last_interface=last_interface)
        relay_mock.assert_called_once_with(first_interface=1, last_interface=3)

    @ patch.object(CiscoEthSwitchPoe, 'set_power_inline')
    def test_set_power_inline(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        state = 'auto'
        interface_id = 3
        relay_conn.set_power_inline(state=state, interface_id=interface_id)
        relay_mock.assert_called_once_with(state='auto', interface_id=3)
        
    @ patch.object(CiscoEthSwitchPoe, 'get_power_inline')
    def test_get_power_inline(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        interface_id = 3
        relay_conn.get_power_inline(interface_id=interface_id)
        relay_mock.assert_called_once_with(interface_id=3)

    @ patch.object(CiscoEthSwitchPoe, 'power_inline_legacy_enable')
    def test_power_inline_legacy_enable(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        state = 'disable'
        relay_conn.power_inline_legacy_enable(state=state)
        relay_mock.assert_called_once_with(state='disable')
        
    @ patch.object(CiscoEthSwitchPoe, 'set_power_inline_limit')
    def test_set_power_inline_limit(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        limit = 20000
        interface_id = 3
        relay_conn.set_power_inline_limit(limit=limit, interface_id=interface_id)
        relay_mock.assert_called_once_with(limit=20000, interface_id=3)
    
    @ patch.object(CiscoEthSwitchPoe, 'set_power_inline_limit_mode')
    def test_set_power_inline_limit_mode(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        mode = 'class'
        relay_conn.set_power_inline_limit_mode(mode=mode)
        relay_mock.assert_called_once_with(mode='class')
        
    @ patch.object(CiscoEthSwitchPoe, 'set_power_inline_priority')
    def test_set_power_inline_priority(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        priority = 'critical'
        interface_id = 3
        relay_conn.set_power_inline_priority(priority=priority, interface_id=interface_id)
        relay_mock.assert_called_once_with(priority='critical', interface_id=3)
    
    @ patch.object(CiscoEthSwitchPoe, 'power_inline_traps_enable')
    def test_power_inline_traps_enable(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        is_enable = False
        relay_conn.power_inline_traps_enable(is_enable=is_enable)
        relay_mock.assert_called_once_with(is_enable=False)
        
    @ patch.object(CiscoEthSwitchPoe, 'set_power_inline_usage_threshold')
    def test_set_power_inline_usage_threshold(self, relay_mock: MagicMock):
        relay_conn = CiscoEthSwitchPoe(username='user',
                                       password='pass',
                                       ip_address='10.0.0.2',
                                       telnet_port=23,
                                       timeout=2)
        threshold = 95
        relay_conn.set_power_inline_usage_threshold(threshold=threshold)
        relay_mock.assert_called_once_with(threshold=95)
    

if __name__ == '__main__':
    unittest.main()
