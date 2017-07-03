driver.implicitly_wait(30)
        driver.find_element_by_css_selector('i.fa.fa-code-fork').click()
        # Clicks duplicate button
        time.sleep(3)
        driver.find_element_by_xpath("//*[contains(text(), 'Fork this Project')]").click()
        # Clicks "Fork this Project" in dropdown
        time.sleep(3)
        driver.find_element_by_xpath("//button[contains(text(), 'Fork')]").click()
        # Clicks "Fork" in "Are you sure you want to fork this project?" modal
        time.sleep(3)
        driver.find_element_by_xpath("//*[contains(text(), 'Go to new fork')]").click()
        # Clicks "Go to new fork" button in modal
        time.sleep(5)
        element = driver.find_element_by_id('nodeTitleEditable')
        # Locates title
        assert element.text == 'Fork of Fork Project'
        # Confirms title reads: "Fork of Fork Project"