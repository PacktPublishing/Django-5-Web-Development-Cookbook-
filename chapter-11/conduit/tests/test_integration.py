from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from factories import UserFactory
import logging

logger = logging.getLogger(__name__)


class TestArticleCreation(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        firefox_options = webdriver.FirefoxOptions()
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub", options=firefox_options
        )
        cls.selenium.implicitly_wait(10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_server_url = "http://host.docker.internal:8000"

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_article(self):
        user = UserFactory()
        logger.debug(f"User: {user}")

        self.selenium.get(f"{self.live_server_url}/login/")
        logger.debug(f"URL: {self.live_server_url}/login")
        self.selenium.find_element(By.ID, "id_username").send_keys(user.email)
        self.selenium.find_element(By.ID, "id_password").send_keys(user.password)
        logger.info("Logging in: ", user.email, user.password)
        self.selenium.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Navigate to article creation page
        WebDriverWait(self.selenium, 10).until(
            EC.url_changes(f"{self.live_server_url}/")
        )
        logger.info("Logged in")
        self.selenium.get(f"{self.live_server_url}/articles/new")
        logger.info("Navigating to create article page")

        # Fill out the article creation form
        self.selenium.find_element(By.NAME, "title").send_keys("Selenium Test Article")
        self.selenium.find_element(By.NAME, "summary").send_keys(
            "Description for the Selenium test article."
        )
        self.selenium.find_element(By.NAME, "content").send_keys(
            "Content for the Selenium test article."
        )
        logger.info("Filling out the article creation form")
        # self.selenium.find_element(By.NAME, "submit").click()
        submit = self.selenium.find_element(By.ID, "id_submit")

        submit.click()

        logger.info("Submitting the form")

        # Verify the article was created
        WebDriverWait(self.selenium, 10).until(
            EC.url_changes(f"{self.live_server_url}/articles")
        )
        self.selenium.get(f"{self.live_server_url}/articles")

        assert "Selenium Test Article" in self.selenium.page_source
