import os
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml
from device_mapping import device_ip_mapping
import subprocess

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def render_template(template_path, data):
    env = Environment(loader=FileSystemLoader('../../jinja_templates/ciscoxr'))
    template = env.get_template(template_path)
    return template.render(data)

def load_config(device_ip, device_port, device_username, device_password, config_data):
    try:

        device_info = {
            'device_type': 'cisco_xr',
            'ip': device_ip,
            'port': device_port,
            'username': device_username,
            'password': device_password,
            'secret': device_password,
            'session_log': 'session_output.log',
        }

        with ConnectHandler(**device_info) as ssh:
            print(f"Connected to {device_ip}")

            # Send configuration commands
            output = ssh.send_config_set(config_data)
            print(output)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        device_username = os.environ.get('IOSXR_USERNAME')
        device_password = os.environ.get('IOSXR_PASSWORD')
        device_port = 22

        # Check if environment variables are set
        if device_username is None or device_password is None:
            print("Please set IOSXR_USERNAME and IOSXR_PASSWORD environment variables.")
        else:
            device_name = input('Enter the device name: ').lower()
            # Look up the device IP address from the mapping
            device_ip = device_ip_mapping.get(device_name)
            if device_ip is None:
                print(f"Device with name '{device_name}' not found in the mapping.")
            else:
                # Call base config generator
                base_config_generator = '../../config_generators/ciscoxr/base.py'
                subprocess.run(['python3', base_config_generator, device_name])

                #call ospf config generator
                ospf_config_generator = '../../config_generators/ciscoxr/ospf.py'
                subprocess.run(['python3', ospf_config_generator, device_name])
                print("run bgp generator")
                #call bgp config generator
                bgp_config_generator = '../../config_generators/ciscoxr/bgp.py'
                subprocess.run(['python3', bgp_config_generator, device_name])

                config_file_path = f'../../startup_configs/ciscoxr/{device_name}.conf'
                with open(config_file_path, 'r') as config_file_path:
                    config_data = [line for line in config_file_path.readlines() if line.strip()]
                print('printing configs')
                print(config_data)

                load_config(device_ip, device_port, device_username, device_password, config_data)


    except KeyboardInterrupt:
        print("\nScript execution interrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
