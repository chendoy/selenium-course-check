#!/bin/python3

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import telegram_send

EXTENDED_SEARCH_XPATH = "/html/body/center/d1iv/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/a[2]"
SEARCH_BUTTON_XPATH = "/html/body/center/d1iv/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div/input[1]"
RESULT_XPATH = "//*[@id=\"courseTable\"]/tbody/tr/td[3]/a"
TIMES1_XPATH = "/html/body/center/d1iv/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[12]/td[4]/div"
TIMES2_XPATH = "/html/body/center/d1iv/table[2]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[13]/td[4]/div"
COURSE_NAME_ID = "oc_course_name"
INTERVAL = 3600
driver = None


def main():
    while(True):
        global driver

        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome('./chromedriver')
        driver.get('https://bgu4u.bgu.ac.il/pls/scwp/!app.gate?app=ann')
        frame_switch('main')
        send_click(EXTENDED_SEARCH_XPATH)
        send_text(COURSE_NAME_ID, 'מבוא לתקשורת נתונים')
        send_click(SEARCH_BUTTON_XPATH)
        send_click(RESULT_XPATH)
        times_1 = get_text(TIMES1_XPATH)
        times_2 = get_text(TIMES2_XPATH)
        telegram_send.send(messages=[times_1 + '\n' + times_2])
        driver.close()
        sleep(INTERVAL)
    display.stop()

def get_text(xpath):
    elm = driver.find_element_by_xpath(xpath)
    return elm.text


def send_click(xpath):
    link = driver.find_element_by_xpath(xpath)
    link.click()


def frame_switch(name):
  driver.switch_to.frame(driver.find_element_by_name(name))


def send_return(id):
    form = driver.find_element_by_name(id)
    form.send_keys(Keys.RETURN)


def send_text(id, text):
    form = driver.find_element_by_name(id)
    form.clear()
    form.send_keys(text)


if __name__ == '__main__':
    main()
