from time import sleep

from django.test import TestCase
from selenium import webdriver


class ItemTests(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path='C:\chromedriver.exe')

    def test_item_search(self):
        self.driver.get('http://localhost:8000/search/')
        self.driver.find_element_by_id('id_min_price').send_keys('10')
        self.driver.find_element_by_id('id_max_price').send_keys('1000')
        self.driver.find_element_by_name('is_sold').click()
        self.driver.find_element_by_tag_name('button').click()
        sleep(2)

        rows = self.driver.find_elements_by_tag_name('tr')
        result_ids = [int(row.get_attribute('data-item-id')) for row in rows[1:]]
        self.assertEqual([6,5], result_ids)
# Create your tests here.
