import pytest
from selenium.webdriver.common.keys import Keys

import markers
import settings
from pages.landing import LandingPage
from pages.register import RegisterPage
from pages.search import SearchPage
from pages.user import UserProfilePage


@pytest.fixture()
def landing_page(driver):
    landing_page = LandingPage(driver)
    landing_page.goto_with_reload()
    return landing_page


@markers.smoke_test
class TestHomeLandingPage:
    @markers.core_functionality
    def test_get_started(self, driver, landing_page):
        landing_page.get_started_button.click()
        RegisterPage(driver, verify=True)

    @markers.core_functionality
    def test_search(self, driver, landing_page):
        landing_page.search_input.send_keys('*')
        landing_page.search_input.send_keys(Keys.ENTER)
        search_page = SearchPage(driver, verify=True)
        search_page.loading_indicator.here_then_gone()
        assert search_page.search_results

    @markers.core_functionality
    def test_learn_more(self, driver, landing_page):
        landing_page.learn_more_button.click()
        assert 'https://www.cos.io/products/osf' in driver.current_url

    def test_testimonials_by_buttons(self, driver, landing_page):
        landing_page.scroll_into_view(landing_page.testimonial_3_button.element)
        # Verify that Testimonial 1 slide is initially visible
        assert landing_page.testimonial_1_slide.present()
        assert landing_page.testimonial_2_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Click the button above the testimonial carousel to go to Testimonial 3
        landing_page.testimonial_3_button.click()
        assert landing_page.testimonial_3_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_2_slide.absent()
        # Click the button above the testimonial carousel to go to Testimonial 2
        landing_page.testimonial_2_button.click()
        assert landing_page.testimonial_2_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Click the button above the testimonial carousel to go to Testimonial 1
        landing_page.testimonial_1_button.click()
        assert landing_page.testimonial_1_slide.present()
        assert landing_page.testimonial_2_slide.absent()
        assert landing_page.testimonial_3_slide.absent()

    def test_testimonials_by_arrows(self, driver, landing_page):
        landing_page.scroll_into_view(landing_page.previous_testimonial_arrow.element)
        # Verify that Testimonial 1 slide is initially visible
        assert landing_page.testimonial_1_slide.present()
        assert landing_page.testimonial_2_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Click the previous arrow to the left of the slide to go to Testimonial 3
        landing_page.previous_testimonial_arrow.click()
        assert landing_page.testimonial_3_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_2_slide.absent()
        # Click the previous arrow again to go to Testimonial 2
        landing_page.previous_testimonial_arrow.click()
        assert landing_page.testimonial_2_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Click the previous arrow again to go to Testimonial 1
        landing_page.previous_testimonial_arrow.click()
        assert landing_page.testimonial_1_slide.present()
        assert landing_page.testimonial_2_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Next click the next arrow to the right of the slide to go to Testimonial 2
        landing_page.next_testimonial_arrow.click()
        assert landing_page.testimonial_2_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_3_slide.absent()
        # Click the next arrow again to go to Testimonial 3
        landing_page.next_testimonial_arrow.click()
        assert landing_page.testimonial_3_slide.present()
        assert landing_page.testimonial_1_slide.absent()
        assert landing_page.testimonial_2_slide.absent()

    @pytest.mark.skipif(
        not settings.PRODUCTION,
        reason='User Guids only exist in Production',
    )
    def test_testimonial_1_view_research_link(self, driver, landing_page):
        landing_page.scroll_into_view(landing_page.testimonial_view_research_links[0])
        # Verify that Testimonial 1 slide is initially visible
        assert landing_page.testimonial_1_slide.present()
        # Click the "See her research" link and verify that you are navigated to the User
        # Profile page for Patricia Ayala (guid=wx9bf)
        landing_page.testimonial_view_research_links[0].click()
        UserProfilePage(driver, verify=True)
        assert 'wx9bf' in driver.current_url

    @pytest.mark.skipif(
        not settings.PRODUCTION,
        reason='User Guids only exist in Production',
    )
    def test_testimonial_2_view_research_link(self, driver, landing_page):
        landing_page.scroll_into_view(landing_page.testimonial_view_research_links[0])
        assert landing_page.testimonial_1_slide.present()
        # Click the next arrow to the right of the slide to go to Testimonial 2
        landing_page.next_testimonial_arrow.click()
        assert landing_page.testimonial_2_slide.present()
        # Click the "See her research" link and verify that you are navigated to the User
        # Profile page for Maya Mathur (guid=e9tg8)
        landing_page.testimonial_view_research_links[1].click()
        UserProfilePage(driver, verify=True)
        assert 'e9tg8' in driver.current_url

    @pytest.mark.skipif(
        not settings.PRODUCTION,
        reason='User Guids only exist in Production',
    )
    def test_testimonial_3_view_research_link(self, driver, landing_page):
        landing_page.scroll_into_view(landing_page.testimonial_view_research_links[0])
        assert landing_page.testimonial_1_slide.present()
        # Click the button above the testimonial carousel to go to Testimonial 3
        landing_page.testimonial_3_button.click()
        assert landing_page.testimonial_3_slide.present()
        # Click the "See his research" link and verify that you are navigated to the User
        # Profile page for Philip Cohen (guid=2u4tf)
        landing_page.testimonial_view_research_links[2].click()
        UserProfilePage(driver, verify=True)
        assert '2u4tf' in driver.current_url
