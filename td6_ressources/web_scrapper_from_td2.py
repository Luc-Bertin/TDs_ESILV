from selenium import webdriver #the webdriver package
from selenium.webdriver.common.by import By #use the method to select
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait #enables to wait until condition is fullfilled or just until a timeout exception is returned
from selenium.webdriver.support import expected_conditions as ec #enables to create the conditions
from selenium.common.exceptions import TimeoutException #enables to retrieve the exceptions type
from selenium.common.exceptions import NoSuchElementException #enables to retrieve the exceptions type

import time

class NbCallFunction:
    """ This is a decorator to count the number of times a function has been called
    It will be used to retrieve the image number to put it in working directory"""
    def __init__(self, function):
        self.callNumber = 0
        self.function = function
    def __call__(self, *args, **kwargs):
        ## onCall
        self.callNumber += 1
        return self.function(*args, **kwargs)




class WebScraper:
    def __init__(self, hashtag=None):
        ## Options for the web driver (here incognito mode for Chrome, better to be prompted again the password each time we open a new web-browser)
        options = webdriver.ChromeOptions()
        options.add_argument(' - incognito')
        ## Get the webdriver from its location path
        self.driver = webdriver.Chrome(executable_path='./chromedriver', options = options)
        if hashtag is not None:
            self._hashtag = hashtag

    def enter_credentials(self, id, password):
        """ enter credentials in home page """
        ## Go to Instagram main connection page
        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        ## Define a callable functino which waits element to load
        WebDriverWait(self.driver, timeout=1000).until(ec.visibility_of_all_elements_located((By.TAG_NAME, 'input')))
        ## Enter ID/password
        self.driver.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys(id) #insta.USER_ID
        self.driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(password) #insta.USER_PASSWORD
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        ## Delete pop-up
        ButtonPopup = WebDriverWait(self.driver, timeout=5).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']")))
        ButtonPopup[0].click()

    @property
    def hashtag(self):
        print("Provided hashtag : {}\n".format(self._hashtag))
        return self._hashtag

    @hashtag.setter
    def hashtag(self, value):
        self._hashtag = value

    @staticmethod
    @NbCallFunction
    def download_img_from_link(string_url_img, hashtag_name):
        """ This function retrieve all the photos from the visible window"""
        import os
        import requests as req
        path = 'data_' + hashtag_name.lstrip('#') + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        string_path = path + str(WebScraper.download_img_from_link.callNumber) + '.jpg'
        with open(string_path, 'wb') as file:
            response = req.get(string_url_img)
            print(response) if (not response.ok) else file.write(response.content)


    def run(self, limit_rate=10):
        """ Crawl webpage based on provided hashtag to retrieve all photos """
        search_bar = self.driver.find_element(By.CSS_SELECTOR, "input[class='XTCLo x3qfX ']")
        search_bar.send_keys(self._hashtag)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(3)
        ## sometimes we have to press multiple times Enter...
        search_bar.send_keys(Keys.ENTER)
        search_bar.send_keys(Keys.ENTER)
        search_bar.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, timeout=10).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w']")))

        ##==== the while loop idea using the last_height and new_height is from @Artjom B. on Stackoverflow \
        ##==== i find it quite straightforward and useful ====##
        SLEEP_EACH_SCROLL, nb_scrolls = 3, 0
        #last_height = self.driver.execute_script("return document.body.scrollHeight") # Get scroll height executing js script

        all_images_so_far = set()
        while nb_scrolls < limit_rate:
            try:
                ## Scroll down to bottom
                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SLEEP_EACH_SCROLL)

                ## Retrieve the divs list
                liens_images = [ element.get_attribute('src') for element in self.driver.find_elements(By.CSS_SELECTOR, "div[class='v1Nh3 kIKUG  _bz0w'] img")]

                ## important: in case the visible window overlapp with the former one, we don't want photos to get scrapped twice (so we say not in 's')
                string_url_imgs = [self.download_img_from_link(x, self._hashtag) for x in liens_images if x not in all_images_so_far]

                ## Keep note of stored images
                all_images_so_far = all_images_so_far | set(liens_images) # Saving this list to avoid downloading again the same photos
                nb_scrolls += 1

                ## Some printing
                print("scrolling number : " + str(nb_scrolls) + " on limit : " + str(limit_rate))
                print("number of photos downloaded : " + str(self.download_img_from_link.callNumber))
            except Exception as e:
                print(e)
                print('retrying...')
                time.sleep(3)
