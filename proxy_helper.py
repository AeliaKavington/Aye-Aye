import json
import time

POLL_FREQUENCY = 0.5  # How long to sleep inbetween calls to the method
TIMEOUT = 10  # How long to wait until TimeoutError call


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
            value = string
            if value in data:
                return
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutError(message)

    def not_until(self, string, message=''):
        # Wait for resource not appear in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            value = string
            if value in data:
                break
            time.sleep(self._poll)
            if time.time() > end_time:
                return
        if message == '':
            raise ValueError('{} found.'.format(value))
        else:
            raise ValueError(message)

    def before(self, string_first, string_second):
        # Wait for first resource not appear before second resource in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            first = string_first
            second = string_second
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
                        raise ValueError('{} found before \'{}\'.'.format(second, first))
                    else:
                        return
                elif first_date == [] and second_date != []:
                    raise ValueError('{} found before \'{}\'.'.format(second, first))

            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutError('\'{}\' or \'{}\' not found in time.'.format(first, second))

    def not_before(self, string_first, string_second):
        # Wait for first resource not appear before second resource in the HAR until Timeout
        end_time = time.time() + self._timeout
        while True:
            data = json.dumps(self._proxy.har)
            first = string_first
            second = string_second
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
                        raise ValueError('{} found before \'{}\'.'.format(first, second))
                    else:
                        return
                elif first_date != [] and second_date == []:
                    raise ValueError('{} found before \'{}\'.'.format(first, second))

            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutError('\'{}\' or \'{}\' not found in time.'.format(second, first))
