# IOS-XE-MDT

Wireless network monitoring using Cisco 9800 Streaming Telemetry, Docker and TIG

## Instructions:

#### 1. Configuration on the 9800

Open the "9800_telemetry_config_template.txt" file, edit the source and destination IP address to suit your test environment, then copy and paste onto the running configuration of the 9800 (tested with IOS-XE 17.3.3).

#### 2. Copy and paste initial configs for Docker containers

On the host machine where you will build your containers, copy the "docker-compose.yml", "telegraf.conf" and "syslog-ng.conf" file onto their respective directory.  I strongly recommend that you create a separate directory under your root directory path called telegraf, syslog-ng and influxdb2.

#### 3. Edit the docker-compose.yml file

In "docker-compose.yml" file, replace <root-directory-path> with your local directory path name.

#### 4. Launch the containers

Launch the containers using the command

docker-compose up -d

and you should see the following output.
 
bcho@bcho-ubuntu-2:~$ sudo docker-compose up -d 
Pulling grafana (grafana/grafana:latest)... 
latest: Pulling from grafana/grafana 
59bf1c3509f3: Pull complete 
13b4fa0a02a1: Pull complete 
4e10a437560b: Pull complete 
e4d9ca611bac: Pull complete 
177420590967: Pull complete 
9964d34a6ec0: Pull complete 
70efef88a339: Pull complete 
51554308facc: Pull complete 
55f93af2fedd: Pull complete 
0c743e01dd77: Pull complete 
Digest: sha256:688013c1dc30e9f9c8fc77f1ce328994f47923094b627a99ff5a15c427e8dd8f 
Status: Downloaded newer image for grafana/grafana:latest 
Pulling influxdb (influxdb:latest)... 
latest: Pulling from library/influxdb 
7d66b83ec869: Pull complete 
d88439e7b50a: Pull complete 
22360a9558f7: Pull complete 
9b9d2c016e5c: Pull complete 
f676b1914da4: Pull complete 
2fec6e1b6230: Pull complete 
d103a21252e5: Pull complete 
c306a07eeb6f: Pull complete 
76c1726c8842: Pull complete 
f588dc4b1425: Pull complete 
Digest: sha256:799aace0d410205ee8f37041acc6072ca4d5fff643119727a140d213f8ae44c0 
Status: Downloaded newer image for influxdb:latest 
Pulling telegraf (telegraf:latest)... 
latest: Pulling from library/telegraf 
5492f66d2700: Pull complete 
540ff8c0841d: Pull complete 
a0bf850a0df0: Pull complete 
bdde3a56d298: Pull complete 
4eee1cc8a175: Pull complete 
117aa125aa50: Pull complete 
6ae91bf34564: Pull complete 
Digest: sha256:fd87bd05d45f4cf88d647bc9d87a3d64a2823c6fb369ec461fc8db09c08658c8 
Status: Downloaded newer image for telegraf:latest 
Pulling syslog-ng (balabit/syslog-ng:latest)... 
latest: Pulling from balabit/syslog-ng 
b487f29e2f74: Pull complete 
9c03e2b01f37: Pull complete 
39aa4d72d6d3: Pull complete 
ed38f7fa1dbc: Pull complete 
4df1dab4dd26: Pull complete
Digest: sha256:8d8f557fc01101793c7222c2ae19cba64250fcf470721e889f295a476f45dae7 
Status: Downloaded newer image for balabit/syslog-ng:latest 
Creating grafana   ... done 
Creating syslog-ng ... done 
Creating influxdb  ... done 
Creating telegraf  ... done

#### 5. Initial settings for Grafana
 
Access Grafana GUI using the default 'admin/admin' credential.  You will be asked to change the password.

#### 6. Initial settings for Influxdb
 
You then need do setup your Influxdb datastore.  Use the following settings.

Query Language - Flux  
HTTP URL - http://influxdb:8086  
AUTH Basic Auth - Disable  
Organisation - bcho.com  
Token - cisco123  
Bucket - 9800


#### 7. Import Pre-Built Dashboards
 
Next, import the sample dashboards "9800_wifi_telemetry_dashboard_template.json" and "9800_syslog_dashboard.json".

You should now see the 9800 streaming telemetry in Grafana.  Now it's your turn to create your own dashboards.  Good luck!
