This directory contains the configuration information and map-game updater scripts to successfully host a SPADS instance for BAR

Remember to look through the paths to set them correcly for your host, as well as the logins and passwords!

Spads available here: http://planetspads.free.fr/


# Service Script

The spads.service file is for starting single instances of spads hosts.

Use `systemctl start spads.service` to start the service
Use `systemctl enable spads.service` to start the service on startup

The spads@.service file is for starting multiple instances of spads hosts.

Use `systemctl start spads@<hostid>.service` to start the service
Use `systemctl enable spads@<hostid>.service` to start the service on startup
Replacing the <hostid> with the relevant id number

Update the paths in the file/s to suit your system.
