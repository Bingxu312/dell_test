#!/usr/bin/python3

import json
import time
import subprocess

def send_event():
    with open('data.json') as data_file:
        data = json.load(data_file)
        # data_list = list(json.load(f))

    print(type(data))
    print(data)

    # print(data_list)
    print(type(list(data[1].values())))
    print(list(data[1].values())[0][0])

    node = "ABCDE"
    # cmd = curl --unix-socket /var/lib/apexcp/nginx/socket/nginx.sock http://127.0.0.1/rest/apex-cp/internal/az-event-service/v1/events -d '{"appliance_id": "", "node_id": "36JH8Y3", "component_id": "36JH8Y3", "sub_component_id": "", "host_name": "h07s03-n140.delta.local", "params": "", "code": "1140UPDE0004", "event_time": "2023-7-19 04:16:35"}' -H "Content-Type: application/json"
    command = (f'curl --unix-socket /var/lib/apexcp/nginx/socket/nginx.sock http://127.0.0.1/rest/apex-cp/internal/az-event-service/v1/events '
               f'-d \'{{"appliance_id": "{node}", "node_id": "36JH8Y3", "component_id": "36JH8Y3", "sub_component_id": "", '
               f'"host_name": "h07s03-n140.delta.local", "params": "", "code": "1140UPDE0004", "event_time": "2023-7-19 04:16:35"}}\' '
               f'-H "Content-Type: application/json"')

    print(command)

    with open('rules.json') as rule:
        rules = json.load(rule)

    frequency = rules["sending_event_rules"]["frequency"]
    node_id = rules["events_info"]["node_id"]
    print(frequency, node_id)

    global current_code

    codes = [item["code"] for item in data]
    n = 4
    while codes:
        for _ in range(n):
            if not codes:
                break
            code = codes.pop(0)
            print(f'df -d {code}')
            command = f'lhfd'
            subprocess.run(command, shell=True)
            time.sleep(1)
            # return code
        if not codes:
            break
        time.sleep(2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    send_event()

    # if current_code:
    #     command = f'ls'
    #     subprocess.run(command, shell=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
