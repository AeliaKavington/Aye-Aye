import json
import time
from urllib import parse
POLL_FREQUENCY = 0.5  # How long to sleep inbetween calls to the method
TIMEOUT = 10  # How long to wait until TimeoutError call


def print_logs(log):
    print("\nLOGS:")
    for item in log:
        print(parse.unquote(item))

class ProxyWait(object):
    def __init__(self, proxy, timeout=TIMEOUT, poll_frequency=POLL_FREQUENCY):
        self._proxy = proxy
        self._timeout = timeout
        self._poll = poll_frequency
        # avoid the divide by zero
        if self._poll == 0:
            self._poll = POLL_FREQUENCY

    def until(self, string, message=''):
        #  Wait for resource in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            debug = [item['request']['url'] for item in json.loads(data)['log']['entries']
                     if 'log.rutube.ru' in item['request']['url']]
            value = string
            if value in data:
                return
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        print(print_logs(debug))
        raise TimeoutError(message)

    def not_until(self, string, message=''):
        # Wait for resource not appear in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            debug = [item['request']['url'] for item in json.loads(data)['log']['entries']
                     if 'log.rutube.ru' in item['request']['url']]
            value = string
            if value in data:
                break
            time.sleep(self._poll)
            if time.time() > end_time:
                return
        if message == '':
            print(print_logs(debug))
            raise ValueError('{} found.'.format(value))
        else:
            print(print_logs(debug))
            raise ValueError(message)

    def before(self, string_first, string_second):
        # Wait for first resource not appear before second resource in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            first = string_first
            second = string_second
            debug = [item['request']['url'] for item in json.loads(data)['log']['entries']
                     if 'log.rutube.ru' in item['request']['url']]
            if (first in data) or (second in data):
                data = json.loads(data)
                first_date = [item['startedDateTime'] for item in data['log']['entries']
                              if first in item['request']['url']]
                second_date = [item['startedDateTime'] for item in data['log']['entries']
                               if second in item['request']['url']]

                if first_date != [] and second_date == []:
                    return
                elif first_date != [] and second_date != []:
                    if first_date > second_date:
                        print(print_logs(debug))
                        raise ValueError('{} found before \'{}\'.'.format(second, first))
                    else:
                        return
                elif first_date == [] and second_date != []:
                    print(print_logs(debug))
                    raise ValueError('{} found before \'{}\'.'.format(second, first))

            time.sleep(self._poll)
            if time.time() > end_time:
                break
        print(print_logs(debug))
        raise TimeoutError('\'{}\' or \'{}\' not found in time.'.format(first, second))

    def not_before(self, string_first, string_second):
        # Wait for first resource not appear before second resource in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            first = string_first
            second = string_second
            debug = [item['request']['url'] for item in json.loads(data)['log']['entries']
                     if 'log.rutube.ru' in item['request']['url']]
            if (first in data) or (second in data):
                data = json.loads(data)
                first_date = [item['startedDateTime'] for item in data['log']['entries']
                              if first in item['request']['url']]
                second_date = [item['startedDateTime'] for item in data['log']['entries']
                               if second in item['request']['url']]

                if first_date == [] and second_date != []:
                    return
                elif first_date != [] and second_date != []:
                    if first_date < second_date:
                        print(print_logs(debug))
                        raise ValueError('{} found before \'{}\'.'.format(first, second))
                    else:
                        return
                elif first_date != [] and second_date == []:
                    print(print_logs(debug))
                    raise ValueError('{} found before \'{}\'.'.format(first, second))

            time.sleep(self._poll)
            if time.time() > end_time:
                break
        print(print_logs(debug))
        raise TimeoutError('\'{}\' or \'{}\' not found in time.'.format(second, first))
