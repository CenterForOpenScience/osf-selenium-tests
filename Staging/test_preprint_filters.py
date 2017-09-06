from selenium import webdriver
import time

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}
driver = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)


def test_preprint_filters():
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=thesis")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=preprint")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=true")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=false")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=thesis&filter[allow_submissions]=true")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=thesis&filter[allow_submissions]=false")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=preprint&filter[allow_submissions]=true")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[share_publish_type]=preprint&filter[allow_submissions]=false")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=true&filter[share_publish_type]=thesis")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=false&filter[share_publish_type]=thesis")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=true&filter[share_publish_type]=preprint")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.get("https://api.osf.io/v2/preprint_providers/?filter[allow_submissions]=false&filter[share_publish_type]=preprint")
	assert driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/h1')
	time.sleep(10)
	driver.quit()