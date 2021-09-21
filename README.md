# ios-xe-mdt
Wireless monitoring of Cisco 9800 using Model Driven Telemetry, Docker and TIG Stack.

Instructions:

1. Open the "9800_telemetry_config_template.txt" file, edit the source and destination IP address to suit your test environment, then copy and paste onto the running configuration of the 9800 (tested with IOS-XE 17.3.3).

2. On the host machine where you will build your containers, copy the "docker-compose.yml", "telegraf.conf" and "syslog-ng.conf" file onto the directory (either root or your custom directory).
 
3. 
