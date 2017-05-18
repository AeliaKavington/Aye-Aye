import pytest
from browsermobproxy import Server
from appium import webdriver as appium
import get_devices

# Browsermob proxy agent should be started
server = Server('/data/browsermob-proxy-2.1.4/bin/browsermob-proxy')

def pytest_addoption(parser):
    parser.addoption('--device', '-D',
                     action='store',
                     default=get_devices.default_device(),
                     help='run with specified device')

@pytest.fixture
def device(request):
    device = request.config.getoption('--device', '-D')
    if device == 'and1':
        return get_devices.get_device_by_user('and1')
    elif device == 'and2':
        return get_devices.get_device_by_user('and2')
    elif device == 'and3':
        return get_devices.get_device_by_user('and3')
    else:
        get_devices.print_devices()
        pytest.exit('Unknown device: {}'.format(device))


@pytest.fixture
def proxy(request, device):
    try:
        proxy = server.create_proxy(device['proxy'])
    except:
        pytest.exit('Can\'t connect to proxy')
    proxy.new_har('proxy')
    request.addfinalizer(proxy.close)
    return proxy

@pytest.fixture
def driver(request, device):
    try:
        wd = appium.Remote('http://localhost:4723/wd/hub', desired_capabilities = device['capabilities'])
    except:
        pytest.exit('Can\'t connect to appium')
    request.addfinalizer(wd.quit)
    return wd