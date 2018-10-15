from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request


chromedriver = "C:\\Users\\DELL\\Desktop\\chromedriver_new.exe"
driver = webdriver.Chrome(chromedriver)
print(1)
sleep(2)
driver.get("https://www.ynet.co.il/")
print(2)
sleep(2)
driver.execute_script('''window.open("https://images1.ynet.co.il/PicServer5/2018/09/26/8789574/878957146962264640360no.jpg","_blank");''')
print(3)
sleep(2)
driver.switch_to.window(driver.window_handles[1])
print(3)
sleep(2)
urllib.request.urlretrieve(driver.current_url, "local-filename.jpg")
print(4)
sleep(10)
driver.execute_script('''close();''')
print(5)
sleep(2)
input()