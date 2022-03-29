# ios-xe-mdt
Wireless network monitoring using Cisco 9800 Streaming Telemetry, Docker and TIG

Instructions:

1. Open the "9800_telemetry_config_template.txt" file, edit the source and destination IP address to suit your test environment, then copy and paste onto the running configuration of the 9800 (tested with IOS-XE 17.3.3).

2. On the host machine where you will build your containers, copy the "docker-compose.yml", "telegraf.conf" and "syslog-ng.conf" file onto their respective directory.  I strongly recommend that you create a separate directory under your root directory path called telegraf, syslog-ng and influxdb2.
 
3. In "docker-compose.yml" file, replace <root-directory-path> with your local directory path name.

4. Launch the containers using command

docker-compose up -d

5. Access Grafana GUI using the default 'admin/admin' credential.  You will be asked to change the password.

6. You then need do setup your Influxdb datastore.  Use the following settings.

Query Language - Flux

HTTP URL - http://influxdb:8086

AUTH Basic Auth - Disable

Organisation - bcho.com

Token - cisco123

Bucket - 9800


7. Next, import the sample dashboards "9800_wifi_telemetry_dashboard_template.json" and "9800_syslog_dashboard.json".

You are done!  You should now see the 9800 streaming telemetry.
