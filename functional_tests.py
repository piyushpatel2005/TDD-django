from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith goes to check the online todo app.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention todo lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # she is invited to enter a to-do item straight away

        #she types "Buy peacock feathers" into the text box

        # When she hits enter, the page updates, and now the page lists
        # 1.Buy peacock feathers as an item in a to-do list

        # There is still a text box inviting her to add another item. 
        # she enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Done

if __name__ == '__main__':
    unittest.main()