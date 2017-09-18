import settings
from blocks import login
import time

driver = settings.DRIVER

def test_landing_page():

    # Home Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="primary-navigation"]/span').click()
    driver.find_element_by_xpath('//*[@id="navbarScope"]/div/div[1]/div[2]/ul/li[1]/a/b').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/'

    # Preprints Button
    driver.find_element_by_xpath('//*[@id="primary-navigation"]/span').click()
    driver.find_element_by_xpath('//*[@id="navbarScope"]/div/div[1]/div[2]/ul/li[2]/a/b').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/preprints/'

    # Registries Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="primary-navigation"]/span').click()
    driver.find_element_by_xpath('//*[@id="navbarScope"]/div/div[1]/div[2]/ul/li[3]/a/b').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/registries/'

    # Meetings Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="primary-navigation"]/span').click()
    driver.find_element_by_xpath('//*[@id="navbarScope"]/div/div[1]/div[2]/ul/li[4]/a/b').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/meetings/'

    # Search Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[1]/a').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/search/'

    # Support Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[2]/a').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/support/'

    # Donate Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[3]/a').click()
    time.sleep(3)
    assert driver.current_url == 'https://cos.io/donate-to-cos/'

    # Sign Up Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[4]/div/a[1]').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging.osf.io/register/'

    # Sign In Button
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="secondary-navigation"]/ul/li[4]/div/a[2]').click()
    time.sleep(3)
    assert driver.current_url == 'https://staging-accounts.osf.io/login?service=https://staging.osf.io/'

    # Ensure the YouTube video works
    driver.get("https://staging.osf.io/")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="hero-signup"]/div/div[1]/a/i').click()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="YouTubeModalContent"]/div[1]/button').click()

    # Sign up without any fields filled in
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="signupSubmit"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[4]/div[2]/p[1]')
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[3]/p')
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[2]/p')
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[1]/p')

    # Sign up with only the name field filled in
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[1]/input').send_keys('OSF Selenium')
    driver.find_element_by_xpath('//*[@id="signupSubmit"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[4]/div[2]/p[1]')
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[3]/p')
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[2]/p')    

    # Sign up with an incorrect email
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[2]/input').send_keys('OSF Selenium')
    driver.find_element_by_xpath('//*[@id="signupSubmit"]').click()
    time.sleep(3)   
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[2]/p')
    
    # Check the password strength indicator
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[4]/input').send_keys('a')
    assert driver.find_element_by_xpath('//*[@id="front-password-info"]').text == "Very weak"
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[4]/input').send_keys('acxqi14gskq91dka0')
    assert driver.find_element_by_xpath('//*[@id="front-password-info"]').text == "Great!"

    # Check that the various sign up links work correctly
    driver.get("https://staging.osf.io/")
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[6]/small/a[1]').click()
    time.sleep(3)
    assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'
    driver.get("https://staging.osf.io/")
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[6]/small/a[2]').click()
    time.sleep(3)
    assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'
    driver.get("https://staging.osf.io/")
    driver.find_element_by_xpath('//*[@id="signUpScope"]/form/div[6]/small/a[3]').click()
    time.sleep(3)
    assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md#f-cookies'
    driver.get("https://staging.osf.io/")

    # Check that the footer links work correctly
    driver.find_element_by_xpath("/html/body/div[5]/div/div/p/a[1]").click()
    time.sleep(3)
    assert driver.current_url == 'https://cos.io/'
    driver.get("https://staging.osf.io/")
    driver.find_element_by_xpath("/html/body/div[5]/div/div/p/a[2]").click()
    time.sleep(3)
    assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'
    driver.get("https://staging.osf.io/")
    driver.find_element_by_xpath("/html/body/div[5]/div/div/p/a[3]").click()
    time.sleep(3)
    assert driver.current_url == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'
    driver.get("https://staging.osf.io/")

    # Check random elements on the page
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[2]/p/span')
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[1]/div/h2/strong')
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div[2]/div[2]/h3[3]')
    driver.find_element_by_xpath('/html/body/div[3]/div[5]/div/div/div[2]/p')
    driver.find_element_by_xpath('/html/body/div[3]/div[6]/div/div[2]/div[2]/p/small/em')


    driver.quit()