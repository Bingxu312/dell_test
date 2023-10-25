#!/usr/bin/python3

import json
import time
import subprocess

def auto_send_event():
    """
    Execute test tool functionality
    """
    # read json file and get the data we need inside
    with open('sending_rules.json') as rules_file:
        sending_rule = json.load(rules_file)
    with open('iDrac_Event.json') as idrac_event_file:
        idrac_event_data = json.load(idrac_event_file)
    with open('APEX_Events.json') as apex_event_file:
        apex_event_data = json.load(apex_event_file)

    frequency = sending_rule["sending_event_rules"]["frequency"]
    idrac_events_number = sending_rule["sending_event_rules"]["idrac_events_number"]
    apex_events_number = sending_rule["sending_event_rules"]["apex_events_number"]
    node_id = sending_rule["events_info"][0]["node_id"]
    component_id = sending_rule["events_info"][0]["component_id"]
    host_name = sending_rule["events_info"][0]["host_name"]

    # create command based on sending rule
    idrac_event_code = [item["code"] for item in idrac_event_data]
    apex_event_code = [item["code"] for item in apex_event_data]

    while idrac_event_code or apex_event_code:
        # send iDrac event
        for _ in range(idrac_events_number):
            if not idrac_event_code:
                break

            code = idrac_event_code.pop(0)
            send_event_cmd = f'curl --unix-socket /var/lib/apexcp/nginx/socket/nginx.sock http://127.0.0.1/rest/apex-cp/internal/az-event-service/v1/events ' \
                             f'-d \'{{"appliance_id": "", "node_id": "{node_id}", "component_id": "{component_id}", "sub_component_id": "", ' \
                             f'"host_name": "{host_name}", "params": "", "code": "{code}", "event_time": "2023-7-19 04:16:35"}}\' ' \
                             f'-H "Content-Type: application/json"'
            subprocess.run(send_event_cmd, shell=True)
            # interval one second between each sending to prevent errors caused by simultaneous sending
            time.sleep(1)

        # send APEX event
        for _ in range(apex_events_number):
            if not apex_event_code:
                break

            code = apex_event_code.pop(0)
            send_event_cmd = f'curl --unix-socket /var/lib/apexcp/nginx/socket/nginx.sock http://127.0.0.1/rest/apex-cp/internal/az-event-service/v1/events ' \
                             f'-d \'{{"appliance_id": "", "node_id": "{node_id}", "component_id": "{component_id}", "sub_component_id": "", ' \
                             f'"host_name": "{host_name}", "params": "", "code": "{code}", "event_time": "2023-7-19 04:16:35"}}\' ' \
                             f'-H "Content-Type: application/json"'
            subprocess.run(send_event_cmd, shell=True)
            # interval one second between each sending to prevent errors caused by simultaneous sending
            time.sleep(1)

        if not idrac_event_code or not apex_event_code:
            break
        time.sleep(frequency)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    auto_send_event()

    # if current_code:
    #     command = f'ls'
    #     subprocess.run(command, shell=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
