import time
import json
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from scrapy.selector import Selector



class PassQuiz:

    def __init__(self):
        self.url = 'http://elearning.surgeons.org/course/view.php?' \
            'id=127&section=0'
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()

    def sign_in(self):
        """
        Authorization
        """   
        EMAIL = os.getenv('EMAIL')
        EMAIL_PASSWORD = os.getenv('PASSWORD')

        # find and fill inputs in form
        username = self.driver.find_element_by_name("username")
        username.send_keys(EMAIL)
        password = self.driver.find_element_by_name("password")
        password.send_keys(EMAIL_PASSWORD)
        # send form data
        self.driver.find_element_by_id("regularsubmit").click()

    def get_body(self):
        return self.driver.page_source

    def pass_quiz(self):
        """
        """
        driver = self.driver
        driver.get(self.url)

        self.sign_in()

        for s in range(1,5):
            for j in range(1,4):
                driver.get('http://elearning.surgeons.org/course/view.php?id=127&section=0') 
                
                category = driver.find_element_by_xpath(
                    '//li[@id="section-'+str(s)+'"]/div/ul/li['+str(j)+']/div/div/div/div/a')
                category.click()

                for i in range(0,500):
                    re_attempt = driver.find_element_by_xpath(
                        "//input[@value='Re-attempt quiz'] | "
                        "//input[@value='Attempt quiz now']")
                    re_attempt.click()

                    finish_quiz = driver.find_element_by_class_name("endtestlink")
                    finish_quiz.click()

                    finish_all = driver.find_element_by_xpath(
                        "//input[@value='Submit all and finish']")
                    finish_all.click()

                    time.sleep(2)

                    confirm = driver.find_element_by_xpath(
                        "//div[@class='confirmation-dialogue']/div/"
                        "input[@value='Submit all and finish']")
                    confirm.click()

                    finish_review = driver.find_element_by_partial_link_text(
                       'Finish review')
                    finish_review.click()

    def __del__(self):
        pass
        self.driver.delete_all_cookies()
        self.driver.close()
        self.display.stop()

if __name__ == '__main__':
    cv = PassQuiz()
    cv.pass_quiz()
