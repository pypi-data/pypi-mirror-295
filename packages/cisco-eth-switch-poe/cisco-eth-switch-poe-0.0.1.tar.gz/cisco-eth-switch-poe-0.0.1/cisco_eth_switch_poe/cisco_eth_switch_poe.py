from telnetlib import Telnet
import time


class CiscoEthSwitchPoe:
    _power_inline_lim_min = 0
    _power_inline_lim_max = 30000
    _power_inline_usage_thr_min = 1
    _power_inline_usage_thr_max = 99
    
    def __init__(self,
                 username: str='',
                 password: str='',
                 ip_address: str='192.168.1.254',
                 telnet_port: int=23,
                 timeout: int=2) -> None:
        self._username = username
        self._password = password
        self._ip_address = ip_address
        self._telnet_port = telnet_port
        self._timeout = timeout
        
    def switch_login(self) -> bool:
        try:
            self._telnet_conn.read_until(b"Username:")
            self._telnet_conn.write(self._username.encode('ascii') + b"\n")
            self._telnet_conn.read_until(b"Password:")
            self._telnet_conn.write(self._password.encode('ascii') + b"\n")
            print('Telnet logged in!')
            return True
        except Exception as e:
            print(f'Failed to log-in to telnet!: {e}')
            return False
    
    def connect(self) -> bool:
        self._telnet_conn = Telnet(self._ip_address,
                                   self._telnet_port,
                                   timeout=self._timeout)
        return self.switch_login()
        
    def disconnect(self) -> None:
        self._telnet_conn.close()
        print('Telnet connection closed')
    
    def enter_config_mode(self) -> None:
        self._telnet_conn.write(b"configure terminal\n")
        
    def enter_interface_config(self, interface_id: int) -> None:
        self._telnet_conn.write(b"interface gi" + str(interface_id).encode('ascii') + b"\n")
        
    def exit_config_mode(self) -> None:
        self._telnet_conn.write(b"exit\n")
        
    def config_mode(func) -> object:
        def wrapper(self, *args, **kwargs) -> object:
            self.enter_config_mode()
            res = func(self, *args, **kwargs)
            self.exit_config_mode()
            return res
        return wrapper
    
    def interface_config(func) -> object:
        def wrapper(self, *args, **kwargs) -> object:
            self.enter_interface_config(kwargs['interface_id'])
            res = func(self, *args, **kwargs)
            self.exit_config_mode()
            return res
        return wrapper
    
    def show_power_inline(self,
                          first_interface: int=1,
                          last_interface: int=1,
                          show_all: bool=False,
                          timeout: int=10) -> str:
        if show_all:
            command = b"show power inline\n"
        else:
            command = f"show power inline interfaces gi{first_interface}-{last_interface}\n"
            command = command.encode('ascii')
        
        self._telnet_conn.write(command)
        # wait to complete reading buffer
        time.sleep(timeout)
        response = self._telnet_conn.read_very_eager()
        return response.decode('ascii')
    
    def show_power_inline_consumption(self,
                                      first_interface: int=1,
                                      last_interface: int=1,
                                      show_all: bool=False,
                                      timeout: int=10) -> str:
        if show_all:
            command = b"show power inline consumption\n"
        else:
            command = f"show power inline consumption interfaces gi{first_interface}-{last_interface}\n"
            command = command.encode('ascii')
        
        self._telnet_conn.write(command)
        # wait to complete reading buffer
        time.sleep(timeout)
        response = self._telnet_conn.read_very_eager()
        return response.decode('ascii')
    
    @config_mode
    @interface_config
    def set_power_inline(self,
                         state: str='auto',
                         time_range: str='',
                         interface_id: int=1) -> None:
        command = f"power inline {state}" if time_range == '' else f"power inline {state}" + time_range
        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Set power inline at interface {interface_id} to state -> {state}')
    
    @config_mode
    def get_power_inline(self, 
                         interface_id: int=1,
                         timeout: int=5) -> str:
        self._telnet_conn.write(b"do show power inline interface gi" + str(interface_id).encode('ascii') + b"\n")
        time.sleep(timeout)
        response = self._telnet_conn.read_very_eager()
        return response.decode('ascii')
    
    @config_mode
    def power_inline_legacy_enable(self, state: str='enable') -> None:        
        if state == 'enable':
            command = b"power inline legacy enable\n"
        elif state == 'disable':
            command = b"no power inline legacy enable\n"

        self._telnet_conn.write(command)
        print(f'Power inline legacy {state}d')
    
    @config_mode
    @interface_config
    def set_power_inline_limit(self,
                               limit: int=-1,
                               interface_id: int=1) -> None:        
        if self._power_inline_lim_min <= limit <= self._power_inline_lim_max:
            command = f'power inline limit {limit}'
        else:
            command = 'no power inline limit'
            
        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Power inline limit gi{interface_id} set to {limit}' \
            if self._power_inline_lim_min <= limit <= self._power_inline_lim_max else f'Power inline limit disabled gi{interface_id}')
    
    @config_mode
    def set_power_inline_limit_mode(self, mode: str='no') -> None:        
        if mode == 'no':
            command = 'no power inline limit-mode'
        else:
            command = f'power inline limit-mode {mode}'

        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Power inline limit mode set to {mode}' if mode != 'no' else 'Power inline limit mode disabled')

    @config_mode
    @interface_config
    def set_power_inline_priority(self,
                                  priority: str='low',
                                  interface_id: int=1) -> None:
        command = f'power inline priority {priority}'
        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Power inline priority gi{interface_id} set to {priority}')
    
    @config_mode
    def power_inline_traps_enable(self, is_enable: bool=True) -> None:        
        if is_enable:
            command = 'power inline priority enable'
        else:
            command = 'no power inline traps enable'
            
        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Power inline traps enabled' if is_enable else 'Power inline traps disabled')
    
    @config_mode
    def set_power_inline_usage_threshold(self, threshold: int=0) -> None:        
        if threshold == 0:
            command = 'no power inline usage-threshold'
        elif self._power_inline_usage_thr_min <= threshold <= self._power_inline_usage_thr_max: 
            command = f'power inline usage-threshold {threshold}'
        else:
            print(f'Input Value Error: {threshold}')
            return
        
        self._telnet_conn.write(command.encode('ascii') + b"\n")
        print(f'Power inline usage threshold set to {threshold}')
