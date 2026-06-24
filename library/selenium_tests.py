import os
import unittest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")

import django
django.setup()

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from authentication.models import CustomUser


class LoginSeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        user = CustomUser.get_by_email("selenium@test.com")

        if not user:
            user = CustomUser.create(
                email="selenium@test.com",
                password="12345",
                first_name="Selenium",
                last_name="User",
            )
            user.role = 1
            user.is_active = True
            user.save()

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def open_login_page(self):
        self.browser.get(self.live_server_url + reverse("login"))

    def fill_login_form(self, email, password):
        email_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='email'], input[name='username'], input[type='email'], input[type='text']")
            )
        )

        password_input = self.browser.find_element(By.CSS_SELECTOR, "input[type='password']")

        email_input.clear()
        password_input.clear()

        email_input.send_keys(email)
        password_input.send_keys(password)

        submit_button = self.browser.find_element(
            By.CSS_SELECTOR,
            "button[type='submit'], input[type='submit'], button"
        )
        submit_button.click()

    def test_login_logout_and_invalid_login(self):
        self.open_login_page()

        self.fill_login_form("selenium@test.com", "12345")

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("selenium@test.com", body_text)

        self.browser.find_element(By.LINK_TEXT, "Logout").click()

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Login", body_text)

        self.open_login_page()

        self.fill_login_form("wrong@test.com", "wrongpassword")

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Invalid email or password", body_text)


if __name__ == "__main__":
    unittest.main()