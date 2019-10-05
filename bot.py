from selenium import webdriver
import os
import time
import config

class InstagramBot:

    def __init__(self, username, password): #initializes an instance of the InstagramBot and calls the login method
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.tag_url = 'https://www.instagram.com/explore/tags'
        self.driver = webdriver.Chrome('./chromedriver.exe') #boots up an instance of Chrome
        self.login()


    def login(self):
        self.driver.get('%s/accounts/login/' % (self.base_url)) #uses webdriver functions to open up the link
        time.sleep(1)
        self.driver.find_element_by_name('username').send_keys(self.username) #uses the class' username and password to fill in the login info
        self.driver.find_element_by_name('password').send_keys(self.password) 
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click() #presses the login button
        time.sleep(5)


    def nav_tag(self,tag):
        self.driver.get('%s/%s' % (self.tag_url, tag)) #searches up photos with a specific tag


    def nav_user(self, user):
        self.driver.get('%s/%s' % (self.base_url, user)) #relocates to a user's page

    
    def follow_user(self, user): #follows a specific user
        self.nav_user(user)
        follow_button = self.find_button('Follow')[0]
        follow_button.click()


    def unfollow_user(self, user): #unfollows a user if followed
        self.nav_user(user)
        unfollow_button = self.find_button('Following')[0]
        if unfollow_button:
            unfollow_button.click()
            unfollow_confirm = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')[0]
            unfollow_confirm.click()


    def like_posts (self, user, num_posts, like=True): #likes a number of the most recent images of a user
        action = 'Like' if like else 'Unlike'
        self.nav_user(user)
        first_img =self.driver.find_element_by_class_name('eLAPa')
        first_img.click()
        time.sleep(2)
        for x in range(num_posts):
            time.sleep(2)
            self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            self.driver.find_element_by_class_name('HBoOv.coreSpriteRightPaginationArrow').click()
            x+=1

    
    
    def find_button(self, text): #locates a button
        bttns = self.driver.find_elements_by_xpath("//button[contains(text(), %s)]" % (text))
        return bttns


if __name__ == '__main__':
    ig_bot = InstagramBot(config.api_username, config.api_password)
    time.sleep(3)
    ig_bot.like_posts("thxmas_tr", 2)
