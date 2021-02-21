from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from channels.testing import ChannelsLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time


class ReflexTest(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    def create_initial_list(self, item_text):
        self.driver.get(self.live_server_url)
        inputbox = self.driver.find_element_by_id('id_text')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Firefox()
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_complete_reflex(self):
        self._enter_ws_sockpuppet()
        self.create_initial_list('hello')
        time.sleep(1)
        element = self.driver.find_element_by_id('item-1')
        complete_button = self.driver.find_element_by_id('complete-item-1')
        ActionChains(self.driver).click(complete_button).perform()
        WebDriverWait(self.driver, 3).until(lambda _:
            'line-through' in element.get_attribute('class').split(),
            'Complete Reflex was not executed')

    def test_delete_reflex(self):
        self._enter_ws_sockpuppet()
        self.create_initial_list('hello')
        time.sleep(1)
        element = self.driver.find_element_by_id('del-item-1')
        ActionChains(self.driver).click(element).perform()
        time.sleep(1)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_id('item-1')

    def test_edit_reflex(self):
        self._enter_ws_sockpuppet()
        self.create_initial_list('hello')
        time.sleep(1)
        element = self.driver.find_element_by_id('edit-item-1')
        ActionChains(self.driver).click(element).perform()
        time.sleep(1)
        self.driver.find_element_by_id('input-item-1')

    def _enter_ws_sockpuppet(self):
        self.driver.get(self.live_server_url + '/ws/sockpuppet')