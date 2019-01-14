import os
import time

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rallf.sdk import Task
from rallf.tools import SeleniumDeviceFactory


class Twitter(Task):
    def __init__(self, manifest, robot, input, output):
        super().__init__(manifest, robot, input, output)
        self.ffoxProfile = "%s/firefox_profile" % self.home
        self.browser = None
        self.wait = None
        self.wait_for = lambda by, selector: self.wait.until(EC.presence_of_element_located((by, selector)))
        self.wait_for_multi = lambda by, selector: self.wait.until(EC.presence_of_all_elements_located((by, selector)))

    def warmup(self):
        self.logger.info("WARMUP!!!")
        if not os.path.exists(self.ffoxProfile): os.mkdir(self.ffoxProfile)
        factory = SeleniumDeviceFactory(self.robot)
        self.browser = factory.build('firefox63', self.ffoxProfile)
        self.wait = WebDriverWait(self.browser, 10)
        super().warmup()

        assert self.browser is not None
        self.browser.get("https://twitter.com")

    def get_followers(self, input):
        self.logger.debug("get_followers started!")
        fw_xpath = "/html/body/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li[3]/a/span[2]"
        fw_container = self.wait_for(By.XPATH, fw_xpath)
        followers = fw_container.get_attribute("innerHTML")
        # time.sleep(30)
        return followers

    def get_followings(self, input):
        self.logger.debug("get_following started!")
        fw_xpath = '//*[@id="page-container"]/div[1]/div[1]/div/div[2]/ul/li[2]/a/span[2]'
        fw_container = self.wait_for(By.XPATH, fw_xpath)
        followings = fw_container.get_attribute("innerHTML")
        # time.sleep(30)
        return followings

    def go_home(self, input=None):
        home_btn = self.wait_for(By.XPATH, '//*[@id="global-nav-home"]')
        home_btn.click()

    def go_following(self, input=None):
        fw_xpath = '//*[@id="page-container"]/div[1]/div[1]/div/div[2]/ul/li[2]/a/span[2]'
        fw_container = self.wait_for(By.XPATH, fw_xpath)
        fw_container.click()

    def open_user_options(self, input=None):
        user_options_xpath = '//*[@id="page-container"]/div[4]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/button'
        user_options_btn = self.wait_for(By.XPATH, user_options_xpath)
        user_options_btn.click()
        time.sleep(2)

        add_to_list_xpath = '//*[@id="page-container"]/div[4]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/div/div/div/div/ul/li[3]/button'

        add_to_list_btn = self.wait_for(By.XPATH, add_to_list_xpath)
        add_to_list_btn.click()

        self.add_to_list()

    def add_to_list(self, input=None):
        add_to_list_btn = self.wait_for(By.ID, 'list-membership-dialog-body')
        options = add_to_list_btn.find_elements(By.TAG_NAME, 'li')
        if not any([option.get_attribute("checked") == "checked" for option in options]):
            options[7].click()

        self.wait_for(By.XPATH, '//*[@id="list-membership-dialog-dialog"]/div[2]/button/span').click()
        time.sleep(500)

    def follow_by_tweet_keywords(self, input):
        self.logger.debug("search started!")
        new_followers = {}
        visited_profiles = ["https://twitter.com/tocappcom"]
        for keyword in input['keywords']:
            new_followers[keyword] = 0
            self.go_home()
            time.sleep(5)
            search_input = self.wait_for(By.XPATH, '//*[@id="search-query"]')
            search_input.send_keys(keyword)
            search_btn = self.wait_for(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/form/span')
            search_btn.click()

            recientes_btn = self.wait_for(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[2]/div/ul/li[2]/a')
            recientes_btn.click()
            time.sleep(5)
            # save main window
            main_window = self.browser.current_window_handle
            self.logger.debug("main window handle is: %s" % str(main_window))

            scrolls_per_search = 10
            for i in range(scrolls_per_search):
                user_containers = self.wait_for_multi(By.CLASS_NAME, 'FullNameGroup')

                for user_container in user_containers:
                    user_link = user_container.find_element(By.XPATH, "..")
                    scroll_position = self.browser.execute_script('return window.pageYOffset;')
                    self.logger.debug("scroll_position: %d" % scroll_position)
                    user_profile_url = user_link.get_attribute("href")
                    self.logger.debug("href: %s" % user_link.get_attribute("href"))

                    if user_profile_url not in visited_profiles:
                        visited_profiles.append(user_profile_url)
                        coords = user_link.location_once_scrolled_into_view

                        self._blank_window()
                        result = self._follow(user_profile_url)
                        if result['followed']:
                            new_followers[keyword] += 1
                        self._close_and_back(main_window)

        return {"total": sum(new_followers.values()), "new_followers": new_followers}

    def search(self, input):
        self.logger.debug("search started!")
        search_input = self.wait_for(By.XPATH, '//*[@id="search-query"]')
        search_input.send_keys(input['query'])
        search_btn = self.wait_for(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/div/div[3]/div/form/span')
        search_btn.click()

        destacados_btn = self.wait_for(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[2]/div/ul/li[2]/a')
        destacados_btn.click()

        user_containers = self.wait_for_multi(By.CLASS_NAME, 'FullNameGroup')

        # save main window
        main_window = self.browser.current_window_handle

        self.logger.debug("main window handle is: %s" % str(main_window))
        new_followers = 0
        for user_container in user_containers:
            user_link = user_container.find_element(By.XPATH, "..")
            scroll_position = self.browser.execute_script('return window.pageYOffset;')
            self.logger.debug("scroll_position: %d" % scroll_position)
            user_profile_url = user_link.get_attribute("href")
            self.logger.debug("href: %s" % user_link.get_attribute("href"))
            coords = user_link.location_once_scrolled_into_view

            self._blank_window()
            result = self._follow(user_profile_url)
            if result['followed']:
                new_followers += 1
            self._close_and_back(main_window)

        return {"total": sum(new_followers.values()), "new_followers": new_followers}

    def _blank_window(self):
        self.browser.execute_script('window.open("", "_blank");')
        self.browser.switch_to.window(self.browser.window_handles[1])

    def _close_and_back(self, main_window):
        self.browser.close()
        self.browser.switch_to.window(main_window)

    def _follow(self, url):
        try:
            self.browser.get(url)
            #time.sleep(5)
            user_actions_li = self.wait_for(By.CLASS_NAME, "ProfileNav-item--userActions")

            follow_container = user_actions_li.find_element(By.CLASS_NAME, "user-actions-follow-button")

            for btn in follow_container.find_elements(By.TAG_NAME, "button"):
                if btn.value_of_css_property("display") == "block":
                    follow_text = btn.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                    self.logger.debug("Follow Text: %s" % follow_text)
                    if follow_text == "Seguir":
                        btn.click()
                        time.sleep(2)
                        return {"followed": True}
                    return {"followed": False}
        except TimeoutException:
            return {"followed": False}

        return {"followed": False}

    def cooldown(self):
        self.logger.info("cooldown!!!")
        try:
            profile_tmp_path = self.browser.capabilities['moz:profile']
            os.system("cp -r %s/* %s" % (profile_tmp_path, self.ffoxProfile))

            # We delete cache2 directory because makes the browser to eat a lot of memory at startup.
            # Also and doesn't seems to downgrade performance
            os.system("rm -rf %s/cache2" % self.ffoxProfile)
            self.browser.close()
        except WebDriverException:
            self.logger.warning("driver already closed")
