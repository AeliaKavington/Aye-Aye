import pytest
from browsermobproxy import Server
from appium import webdriver as appium
import browser_config

# Browsermob proxy agent should be started
server = Server("/data/browsermob-proxy-2.1.4/bin/browsermob-proxy")

def pytest_addoption(parser):
    parser.addoption("--device",
                     action="store",
                     default=[browser_config.Device2],
                     help="Device. Valid options are an1, an2")

@pytest.fixture
def device(request):
    device = request.config.getoption('--device')
    if device == 'an1':
        return browser_config.Device1
    elif device == 'an2':
        return browser_config.Device2
    else:
        print ('Device not supported!')


@pytest.fixture
def proxy(request, device):
    proxy = server.create_proxy(device['proxy'])
    proxy.new_har("proxy")
    request.addfinalizer(proxy.close)
    return proxy

@pytest.fixture
def driver(request, device):
    wd = appium.Remote('http://localhost:4723/wd/hub', desired_capabilities = device['capabilities'])
    request.addfinalizer(wd.quit)
    return wd