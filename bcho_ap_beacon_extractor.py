import getpass
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paramiko
import re
import time
from time import strftime, localtime

"""
This script will login to the AP in 
"""

def ap_beacon_stat(device_beacon_count, ap_name, slot_id):

    index_num = 0
    for item in device_beacon_count:
        if (item == 'Tx:'):
            beacon_section = device_beacon_count[index_num + 1]
            break
        else:
            beacon_section = '0/0'
        index_num += 1
    beacon_list = []
    beacon_list.append(beacon_section.split('/'))
    TxBeaconTotal = beacon_list[0][0]
    TxBeacon5secAvg = beacon_list[0][1]

    ap_beacon_dict = {
                    "measurement": "ap_beacon",
                    "tags": {
                            "ap_name": ap_name,
                            "slot": slot_id
                            },
                    "fields": {
                            "tx_beacon": int(TxBeaconTotal)
                            }
                    }
    return(ap_beacon_dict)

def device_ssh(d_ip, d_username, d_password):

    # Establish SSH session to AP
    try:
        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(d_ip, username=d_username, password=d_password,
                                timeout=5, look_for_keys=False, allow_agent=False)

    except Exception as e:
        print(strftime("%Y-%m-%d %H:%M:%S %Z", localtime())
              + " Failed logging into {}".format(d_ip))
        remote_conn.transport.close()
        return

    # Disables config paging on the AP
    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(2)

    remote_conn.send("enable\n")
    remote_conn.send(d_password + "\n")
    remote_conn.send("term length 0\n")
    time.sleep(1)
    ap_output = remote_conn.recv(65535)

    # Need to change this to dyn
    APName = "9120-1"
    ap_beacon = []

    # Define how long you want to poll the device
    no_days = 7
    no_hrs = 24
    current_time = int(time.time())
    total_seconds = no_hrs * 60 * 60
    end_time = no_days * no_hrs * 60 * 60 + current_time + total_seconds

    # Integration with influxdb
    my_bucket = "9120-1"
    my_org = "bcho.com"
    client = InfluxDBClient(url="http://10.0.0.106:8086", token="cisco123", org="bcho.com")
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Handles the periodic polling of AP data
    while (current_time < end_time):

        # This section handles the collection of Beacon stats for Slot 0
        remote_conn.send('show controller dot11 0 | i "Beacon"\n')
        time.sleep(10)
        device_output_beacon_slot_0 = remote_conn.recv(65535)
        device_output_beacon_slot_0 = device_output_beacon_slot_0.decode('utf-8', errors='ignore')
        device_beacon_count_slot_0 = []
        device_beacon_count_slot_0.append(device_output_beacon_slot_0.split())
        ap_beacon_slot_0 = ap_beacon_stat(device_beacon_count_slot_0[0], APName, "0")
        print(ap_beacon_slot_0)
        ap_beacon.append(ap_beacon_slot_0)

        # This section handles collection of Beacon stats for Slot 1
        remote_conn.send('show controller dot11 1 | i "Beacon"\n')
        time.sleep(10)
        device_output_beacon_slot_1 = remote_conn.recv(65535)
        device_output_beacon_slot_1 = device_output_beacon_slot_1.decode('utf-8', errors='ignore')
        device_beacon_count_slot_1 = []
        device_beacon_count_slot_1.append(device_output_beacon_slot_1.split())
        ap_beacon_slot_1 = ap_beacon_stat(device_beacon_count_slot_1[0], APName, "1")
        print(ap_beacon_slot_1)
        ap_beacon.append(ap_beacon_slot_1)

        # Comment printing below if you don't need to see the script running in the background
        # parsed = json.dumps(ap_noise_dict, indent=4, sort_keys=True)
        # print(json.dumps(ap_beacon_dict, indent=4, sort_keys=False))
        # print(ap_noise_json)
        write_api.write(my_bucket, my_org, ap_beacon)
        write_api.close()

        # This sleep time below plus script cycle run time dictates how often we poll the info from AP
        # Modify as required to increase or decrease this frequency
        time.sleep(12)

        current_time = int(time.time())

    remote_conn.transport.close()

    return()

if __name__ == "__main__":

    # Prompt user with input that will be used by the script
    device_ip = input("AP management IP address: ")
    device_username = input("Device username: ")
    device_password = getpass.getpass("Device password: ")

    device_ssh(device_ip, device_username, device_password)