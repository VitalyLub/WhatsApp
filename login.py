from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
from time import sleep
import urllib.request

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def handle_image_url(link):
    start = find_nth(link, '"', 1)
    end = find_nth(link, '"', 2)
    return link[start+1:end].replace("amp;", "").replace("t=s", "t=l")


def download_image(url):
    urllib.request.urlretrieve(url, "C:\\Users\\DELL\\Desktop\\local-filename.jpg")


def login():
    chromedriver = "C:\\Users\\DELL\\Desktop\\chromedriver_new.exe"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://web.whatsapp.com/")

    print("INSERT QR")
    input()

    # move to friends tab
    driver.find_elements_by_class_name("rAUz7")[1].click()
    sleep(randint(5, 10))

    # print some text in search input box
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input').send_keys('איילון שפירא')
    sleep(randint(5, 10))

    if len(driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]')) == 0:
        no_contact_found = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]').text
        print(no_contact_found)
    else:
        all_row_text = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div').text
        print("all_row_text:", all_row_text)
        if "\n" in all_row_text:
            contact_name, status_text = all_row_text.splitlines()
        else:
            contact_name, status_text = all_row_text, ""
        print("contact name:", contact_name)
        print("status text:", status_text)

        if driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div/div[1]/div/img') == 0:
            src_pic = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div/div[1]/div/img').get_attribute("outerHTML")
            good_url = handle_image_url(src_pic)
            print(good_url)
            sleep(randint(5, 10))
            # open the picture in new tab
            driver.execute_script('''window.open("''' + good_url + '''","_blank");''')
            sleep(randint(5, 10))
            driver.switch_to.window(driver.window_handles[1])
            sleep(randint(5, 10))
            # make screenshot
            driver.save_screenshot("yo.jpeg")
            sleep(randint(5, 10))
            # close the new tab
            driver.execute_script('''window.close();''')
            sleep(randint(5, 10))
            driver.switch_to.window(driver.window_handles[0])
        else:
            print("not found photo")
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input').clear()
        driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input').send_keys('macabi zona')

        # download_image(good_url)
        print("DOWNLOADED")


    input()

def main():
    login()

if __name__ == '__main__':
    main()