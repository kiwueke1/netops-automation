import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import subprocess
from device_mapping import device_ip_mapping

def load_config_to_device(device_ip, device_username, device_password, device_name):
    try:
        # Connect to the Juniper device
        with Device(host=device_ip, user=device_username, password=device_password) as dev:
            print(f"Connected to {dev.hostname}")

            # Construct the path to the configuration file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            startup_configs_folder = os.path.join(parent_dir, 'startup_configs')
            config_file = f'../../startup_configs/juniper/{device_name}.conf'
            file_path = os.path.join(startup_configs_folder, config_file)

            # Open the configuration file
            with open(config_file, 'r') as file:
                device_config = file.read()

            # Load the configuration onto the device
            with Config(dev, mode='exclusive') as cu:
                cu.load(device_config, overwrite=True)
                cu.commit()
                print("Configuration loaded successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Access environment variables
        username = os.environ.get('JUNIPER_USERNAME')
        password = os.environ.get('JUNIPER_PASSWORD')

        # Check if environment variables are set
        if username is None or password is None:
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

                # Call the main function
                load_config_to_device(device_ip, username, password, device_name)

    except KeyboardInterrupt:
        print("\nScript execution interrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
