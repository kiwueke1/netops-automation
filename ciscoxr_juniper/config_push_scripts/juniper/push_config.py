import os
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml
from device_mapping import device_ip_mapping
import subprocess

def load_config(device_ip, device_port, device_username, device_password, config_data):
    try:

        device_info = {
            'device_type': 'juniper_junos',
            'ip': device_ip,
            'port': device_port,
            'username': device_username,
            'password': device_password,
            'secret': device_password,
            'session_log': 'session_output.log',
            'timeout': 60,
            'find_prompt': 'a'
        }

        with ConnectHandler(**device_info) as ssh:
            print(f"Connected to {device_ip}")

            # Send configuration commands
            output = ssh.send_config_set(config_data)
            print(output)
            session_log = net_connect.session_log
            print("sess log here")
            print(session_log)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Access environment variables
        device_username = os.environ.get('JUNIPER_USERNAME')
        device_password = os.environ.get('JUNIPER_PASSWORD')
        device_port = 22

        # Check if environment variables are set
        if device_username is None or device_password is None:
            print("Please set JUNIPER_USERNAME and JUNIPER_PASSWORD environment variables.")
        else:
            # Get user input for the device name
            device_name = input('Enter the device name: ').lower()  # Convert to lowercase for case-insensitive matching

            # Look up the device IP address from the mapping
            device_ip = device_ip_mapping.get(device_name)

            if device_ip is None:
                print(f"Device with name '{device_name}' not found in the mapping.")
            else:
                # Call individual config generators
                base_config_generator = '../../config_generators/juniper/base.py'
                subprocess.run(['python3', base_config_generator, device_name])
                ospf_generator = '../../config_generators/juniper/ospf.py'
                # subprocess.run(['python3', ospf_generator, device_name])
                bgp_generator = '../../config_generators/juniper/bgp.py'
                subprocess.run(['python3', bgp_generator, device_name])
                config_file_path = f'../../startup_configs/juniper/{device_name}.conf'
                with open(config_file_path, 'r') as config_file_path:
                    config_data = [line for line in config_file_path.readlines() if line.strip()]                

                # Call the main function
                load_config(device_ip, device_port, device_username, device_password, config_data)

    except KeyboardInterrupt:
        print("\nScript execution interrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
