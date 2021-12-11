from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# class NewVisitorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retreive_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('lista',header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('PLACEHOLDER'),'wpisz rzecz do zrobienia')


        inputbox.send_keys('kupić pawie pióra')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: kupić pawie pióra')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('zrobic przynety')
        inputbox.send_keys(Keys.ENTER)
        # self.browser.implicitly_wait(3000)

        time.sleep(3)
        #

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('2: zrobic przynety')
        self.check_for_row_in_list_table('1: kupić pawie pióra')


        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('kupić pawie pióra',page_text)
        self.assertNotIn('zrobic przynety',page_text)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('kupić mleko')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('kupić pawie pióra',page_text)
        self.assertIn('kupić mleko',page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)

        inputbox.send_keys('testing\n')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)
