import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDWait
from selenium.webdriver.support import expected_conditions as EC

def test_start_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    WDWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    WDWait(driver, 20).until(EC.presence_of_element_located((By.ID, "skip_time")))
    sleep(2)
    har = json.dumps(proxy.har)
    assert "autotest/impression1" in har
    assert "autotest/impression2" in har
    assert "autotest/creativeView1" in har
    assert "autotest/creativeView2" in har
    assert "autotest/start1" in har
    assert "autotest/start2" in har


def test_play_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    WDWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    WDWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "vjs-share-control")))
    har = json.dumps(proxy.har)
    assert "autotest/firstQuartile1" in har
    assert "autotest/firstQuartile2" in har
    assert "autotest/midpoint1" in har
    assert "autotest/midpoint2" in har
    assert "autotest/thirdQuartile1" in har
    assert "autotest/thirdQuartile2" in har
    assert "autotest/complete1" in har
    assert "autotest/complete2" in har


def test_close_events(proxy, driver):
    driver.get("http://rutube.ru/play/embed/f11ed452bae00f75376a50e0272df71a/")
    WDWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "vjs-play-control")))
    driver.find_element_by_class_name("vjs-play-control").click()
    WDWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "skip_time")))
    driver.find_element_by_id("skip_time").click()
    WDWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "vjs-share-control")))
    har = json.dumps(proxy.har)
    assert "autotest/close1" in har
    assert "autotest/close2" in har