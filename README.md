# INE v5 Advanced Technologies Lab loader

## General Info
This is a simple python/flask webapp that is used to load up the configs in the INE v5 Advanced Technology Lab workbook.  It has been used with virtual hardware in GNS3, but should run fine in any physical or virtual setup.  The backend process is using netmiko to communicate with the devices via a dedicated management VRF.  This prevents the management traffic from influencing the labs in any way.

### File list
* lab.py - main python script with flask and netmiko code
* utils.py - script used to generate some dictionaries for device name and IP mapping, as well as file system directory info.  The device IP to name mapping is hard coded in this file.  Edit the devices dictionary with the appropriate IP info for your setup.
* fix-configs.py - python script used to add MGMT vrf and MGMT ip info in devices, fix interface numbers(prefix 0/), update VTY config, update http client source, and a few other updates
### Directory List
* templates - html/jinja2 files uses to generate HTML for web interface
* static - css for html
* topologies - empty by default, extract the INE config files here.


## Preparing the lab setup - GNS3
The INE labs utilized subinterfaces to "virtually" connected devices together from a Layer 3 perspective.  This allows a single physical topology to support all the labs.  I ran into a few minor issues in getting the v5 config files in GNS3 on newer iosv devices.  The interface names did not inlcude the 0 and slash, so I needed to update the configs to include that.  Also, some of the configs were in UTF-8 format and some were ASCII.  This caused some minor issues as well.  I wrote a preparation script to prepare the config files.

The first step is getting the topology physically connected.  I used gig0/1(which maps to gig1) in the config files as the interface that connects the devices together for the labs.  Basically follow the topology setup that INE has in the guides.  I also am using interface gig0/0 for management.  This is the inteface that I use to telnet into the devices as well as the interface that netmiko uses to communicate.  Pretty easy setup, just configure a switch and plug gig0/0 on all devices into this switch.

Run the fix-configs.py script to prepare the config files.  This script will look at all subdirectories in the topologies directory.  It will open the files and update the configs with the necessary changes to make the lab work.  The IP address that is assigned to the gig0/0 interface in the MGMT vrf is read from the utils.py file.  Update this file before running this script.  The switch configs in the labs don't update correctly.  Because there are so few labs that use the switches, I didn't really care.  If any config is not updated properly, it will spit out the directory and file name to stdout.

Create a "base" config for all device and load on all devices.  Use R1 in the base.configs as a template for the rest.  Make sure the base config is the startup config on all devices.

## Running the lab


