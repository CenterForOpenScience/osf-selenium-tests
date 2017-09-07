from selenium import webdriver
import time

desired_cap = {'browser': 'Chrome', 'browser_version': '59.0', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1920x1080'}
driver = webdriver.Remote(
command_executor='http://osfselenium1:9asHrZGoyk7Tesx9agX5@hub.browserstack.com:80/wd/hub',
desired_capabilities=desired_cap)

def test_landing_page():

	# basically clicks on every single button on the page.
	driver.get("https://staging.osf.io/")
	driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[4]/div/a[2]').click()
	driver.find_element_by_xpath('//*[@id="rememberMe"]').click()
	driver.find_element_by_xpath('//*[@id="rememberMe"]').click()
	driver.find_element_by_xpath('//*[@id="forgot-password"]').click()
	assert driver.current_url == 'https://staging.osf.io/forgotpassword/'
	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')
	driver.find_element_by_xpath('//*[@id="alternative-institution"]').click()
	assert driver.current_url == 'https://staging-accounts.osf.io/login?campaign=institution&service=https%3A%2F%2Fstaging.osf.io%2F'
	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')
	driver.find_element_by_xpath('//*[@id="back-to-osf"]').click()
	assert driver.current_url == 'https://staging.osf.io/'
	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')
	driver.find_element_by_xpath('//*[@id="fm1"]/section[5]/a').click()
	assert driver.current_url == 'https://orcid.org/oauth/signin?client_id=APP-0D8MTONZ6PGNNIRH&scope=%2Fauthenticate&response_type=code&redirect_uri=https%3A%2F%2Fstaging-accounts.osf.io%2Flogin%3Fclient_name%3DOrcidClient#show_login'
	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')


	# tries a primary email and a secondary email.
	driver.find_element_by_xpath('//*[@id="username"]').send_keys('osframeworktesting+ghost@gmail.com')
	driver.find_element_by_xpath('//*[@id="password"]').send_keys('"Repr0duce!"')
	driver.find_element_by_xpath('//*[@id="fm1"]/section[3]/input[4]').click()
	time.sleep(5)
	assert driver.find_element_by_xpath('//*[@id="osfHome"]/div[3]/div/div/div/div/div[1]/h2')
	driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[5]/button').click()
	driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[5]/ul/li[4]/a').click()

	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')
	driver.find_element_by_xpath('//*[@id="username"]').send_keys('osframeworktesting+ghost2@gmail.com')
	driver.find_element_by_xpath('//*[@id="password"]').send_keys('"Repr0duce!"')
	driver.find_element_by_xpath('//*[@id="fm1"]/section[3]/input[4]').click()
	time.sleep(5)
	assert driver.find_element_by_xpath('//*[@id="osfHome"]/div[3]/div/div/div/div/div[1]/h2')

	driver.quit()