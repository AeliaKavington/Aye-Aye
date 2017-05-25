from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as DriverWait

from proxy_helper import ProxyWait


def test_start_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    DriverWait(driver, 30).until(ec.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    ProxyWait(proxy, 15).until("autotest/impression1")
    ProxyWait(proxy, 15).until("autotest/impression2")
    ProxyWait(proxy, 15).until("autotest/creativeView1")
    ProxyWait(proxy, 15).until("autotest/creativeView2")
    ProxyWait(proxy, 15).until("autotest/start1")
    ProxyWait(proxy, 15).until("autotest/start2")


def test_play_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    DriverWait(driver, 30).until(ec.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    ProxyWait(proxy, 15).until("autotest/firstQuartile1")
    ProxyWait(proxy, 15).until("autotest/firstQuartile2")
    ProxyWait(proxy, 15).until("autotest/midpoint1")
    ProxyWait(proxy, 15).until("autotest/midpoint2")
    ProxyWait(proxy, 15).until("autotest/thirdQuartile1")
    ProxyWait(proxy, 15).until("autotest/thirdQuartile2")
    ProxyWait(proxy, 15).until("autotest/complete1")
    ProxyWait(proxy, 15).until("autotest/complete2")
    ProxyWait(proxy, 15).before("autotest/start1", "autotest/firstQuartile1")
    ProxyWait(proxy, 15).before("autotest/firstQuartile1", "autotest/midpoint1")
    ProxyWait(proxy, 15).before("autotest/midpoint1", "autotest/thirdQuartile11")
    ProxyWait(proxy, 15).before("autotest/thirdQuartile1", "autotest/complete1")


def test_close_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    DriverWait(driver, 30).until(ec.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    DriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, "skip_time")))
    driver.find_element_by_id("skip_time").click()
    ProxyWait(proxy, 10).until("autotest/close1")
    ProxyWait(proxy, 10).until("autotest/close2")
