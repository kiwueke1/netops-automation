#Network Configuration Automation Toolkit for CiscoXR and Juniper
##Overview
This toolkit is designed for automating the generation and deployment of network configurations for CiscoXR and Juniper devices. It leverages Jinja templates for configuration syntax, YAML files for variables, and Python scripts for processing and deployment.

##Structure and Components
The codebase is organized into several directories, each serving a specific purpose:

###1. startup_configs
Contains the final configuration files for network devices. These configurations are generated and stored here by the toolkit.

####ciscoxr: Configurations for CiscoXR devices.
####juniper: Configurations for Juniper devices.
###2. yaml_files
Holds YAML files that define variables for generating configurations. Each YAML file corresponds to a specific network device.

ciscoxr: Variable files for CiscoXR devices.
juniper: Variable files for Juniper devices.
3. jinja_templates
Contains Jinja templates that define the structure and syntax of network configurations.

ciscoxr: Templates for CiscoXR devices.
juniper: Templates for Juniper devices.
4. config_generators
Python scripts that generate device configurations by rendering Jinja templates with variables from YAML files.

ciscoxr: Scripts for CiscoXR configurations.
juniper: Scripts for Juniper configurations.
5. config_push_scripts
Scripts and tools for deploying configurations to network devices. The config_push.py in each device's folder is the main script to be run by the user.

ciscoxr: Deployment scripts for CiscoXR.
juniper: Deployment scripts for Juniper.
device_mapping.py: Maps device names to their respective IP addresses.
Usage Instructions
To generate and deploy configurations for a specific device:

Run config_push.py:

Located in config_push_scripts/ciscoxr or config_push_scripts/juniper.
This script prompts for the device name and uses device_mapping.py to find the corresponding IP address.
YAML Files and Jinja Templates:

Ensure the YAML file for the target device is correctly set up in yaml_files.
Jinja templates in jinja_templates are used for the configuration structure.
Automatic Generation and Deployment:

The config_push.py script automatically calls relevant scripts in config_generators to create configurations using the Jinja templates and YAML files.
Generated configurations are stored in startup_configs and then pushed to the devices.
Customization and Extension
Jinja Templates: Modify or add new templates in jinja_templates for different configuration structures.
YAML Variables: Update or add new YAML files in yaml_files for different devices.
Adding New Devices: Update device_mapping.py with new device names and IP addresses.
Troubleshooting and Logs
Check session_output.log in config_push_scripts for logs of configuration deployment.
