# INE v5 Advanced Technologies Lab loader

### General Info
This is a simple python/flask webapp that is used to load up the configs in the INE v5 Advanced Technology Lab workbook.  It has been used with virtual hardware in GNS3, but should run fine in any physical or virtual setup.  The backend process is using netmiko to communicate with the devices via a dedicated management VRF.  This prevents the management traffic from influencing the labs in any way.

### Preparing the lab setup - GNS3
The INE labs utilized subinterfacs to "virtually" connected devices together from a Layer 3 perspective.  This allows a single physical topology to support all the labs.  I ran into a few minor issues in getting the v5 config files in GNS3 on newer iosv devices.  The interface names did not inlcude the 0 and slash, so I needed to update the configs to include that.  Also, some of the configs were in UTF-8 format and some were ASCII.  This caused some minor issues as well.  I wrote a preparation script to prepare the config files.
* Build up the lab


