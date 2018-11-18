__author__ = '10185'
from selenium import webdriver

browser = webdriver.Chrome(executable_path="C:\python flies\myspider\chromedriver.exe")

browser.get("https://www.zhihu.com/signup?next=%2F")

browser.find_element_by_xpath("//div[@class='SignContainer-switch']/span").click()
browser.find_element_by_css_selector(".Login-content input[name='username']").send_keys("13650098286")
browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("chrispaul520")
browser.find_element_by_css_selector(".Login-content button[type='submit']").click()