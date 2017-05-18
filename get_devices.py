from subprocess import check_output
import json

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

def default_device():
    return settings[0]['id']

def get_device_by_user(id):
    for device in settings:
        if id == device['id']:
            device_id = device
    return device_id

def get_connected_devices():
    raw_adb_devices = check_output(["adb", "devices"])
    adb_devices = raw_adb_devices.decode('utf-8').partition('\n')[2].replace('device','').split()
    return adb_devices

def get_known_devices():
    device_list = []
    for device in settings:
        device_list.append([device['id'], device['capabilities']['deviceName'], device['brand'], device['name']])
    return device_list

def print_devices():
    print ('\nKnown devices:')
    for device in get_known_devices():
        print('{} ({}): {} {}'.format (device[0], device[1], device[2], device[3]))
    print ('\nConnected devices:')
    if get_connected_devices():
        for c_device in get_connected_devices():
            for k_device in get_known_devices():
                if k_device[1] == c_device:
                    print('{} ({}): {} {}'.format (k_device[0], k_device[1], k_device[2], k_device[3]))
    else:
        print ('No connected devices')