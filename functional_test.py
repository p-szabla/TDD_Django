from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
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
        self.browser.get('http://localhost:8000')
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('lista',header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('PLACEHOLDER'),'wpisz rzecz do zrobienia')


        inputbox.send_keys('kupić pawie pióra')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(10)
        self.check_for_row_in_list_table('1: kupić pawie pióra')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('zrobic przynety')
        inputbox.send_keys(Keys.ENTER)
        # self.browser.implicitly_wait(3000)

        time.sleep(10)
        #

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: kupić pawie pióra')
        self.check_for_row_in_list_table('2: zrobic przynety')



if __name__ == '__main__':
    unittest.main(warnings='ignore')
# ftp://ftp.helion.pl/przyklady/tddwpr.zip
