import settings
import time

driver = settings.DRIVER

def test_sign_in():

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
	driver.find_element_by_xpath('//*[@id="username"]').send_keys(settings.USERNAME_ONE)
	driver.find_element_by_xpath('//*[@id="password"]').send_keys(settings.PASSWORD)
	driver.find_element_by_xpath('//*[@id="fm1"]/section[3]/input[4]').click()
	time.sleep(5)
	assert driver.find_element_by_xpath('//*[@id="osfHome"]/div[3]/div/div/div/div/div[1]/h2')
	driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[5]/button').click()
	driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[5]/ul/li[4]/a').click()

	driver.get('https://staging-accounts.osf.io/login?service=https://staging.osf.io/')
	driver.find_element_by_xpath('//*[@id="username"]').send_keys(settings.USERNAME_TWO)
	driver.find_element_by_xpath('//*[@id="password"]').send_keys(settings.PASSWORD)
	driver.find_element_by_xpath('//*[@id="fm1"]/section[3]/input[4]').click()
	time.sleep(5)
	assert driver.find_element_by_xpath('//*[@id="osfHome"]/div[3]/div/div/div/div/div[1]/h2')

	driver.quit()