DATA = ["16095043245","16096360015","16096366415","18563970741","18563974742","18563976459","18563977280","18563979964","18564080442","18564084661","18564084753","18565710465","18565712664","18565712734","18565713848","18565714891","18565715063","18565715115","18565716604","18565717009","18565717110","18565717137","18565717500","18565719252","18565719603","18565719949","18564088593","18564089117","18564089128","18568831490","18568833383","18568834757","18566761610","18566761991","18566763879","18566766140","18569522327","18569868277","16095044477","16095045084","16095047330","16095047546","16096364215","16096369530","16096369781","16098410456","16098410769","16098410813","18563970737","18563970739","18563973905","18563974746","18563975871","18563976130","18563976448","18563977275","18564080065","18564080436","18564080535","18564084914","18565711622","18565712656","18565712731","18565712746","18565713846","18565715433","18565715438","18565715440","18565715444","18565715449","18565715600","18565716200","18565716344","18565716363","18565716607","18565716608","18565716609","18565716676","18565716853","18565716863","18565716864","18565716923","18565716927","18565716930","18565716946","18565716948","18565716951","18565716952","18565716953","18565716956","18565716957","18565716958","18565717011","18565717060","18565717120","18565717136","18565717140","18565717141","18565717142","18565717151","18565717457","18565717502","18565717591","18565717593","18565717727","18565717796","18565717892","18565718199","18565718879","18565719247","18565719248","18565719602","18565719837","18565719948","18565719969","18564088339","18564088719","18564088720","18564089083","18564089100","18564089103","18564089104","18564089133","18564089139","18564089140","18568831076","18568831492","18568833335","18568833380","18568836901","18568837682","18568837922","18568838787","18566761382","18566763255","18566763655","18566765472","18566766232","18566768831","18566769410","18569520994","18569524050","18569524770","18569525259","18569525260","18569526480","18569529524","18569529780","18569860004","18569860300","18569860774","18569861271","18569862512","18569864252","18569867345"]

from selenium import webdriver
from random import randint
from time import sleep
import urllib.request
import csv
from datetime import datetime


def handle_image_url(link):
    link = link[link.find('https:'):link.find('draggable') - 1]
    return link.replace("amp;", "").replace("t=s", "t=l")[:-1]


def scrape_number(driver, number):
    # print some text in search input box
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input').send_keys('Camden' + str(number))
    sleep(randint(2, 3))

    row = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), number]

    start_text_log =  "START, " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + str(number)
    print(start_text_log)
    with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
        myfile.write(start_text_log + "\n")

    if 'No results found for' in driver.page_source:
        # no_contact_found = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]').text
        print("not found")
        with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + "not found" + "\n")
        row.extend([-1, -1, -1])
    else:
        sleep(randint(3, 5))
        #'//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]'
        all_row_text = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]').text
        print(all_row_text)
        with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + "all_row_text" + "\n")

        if "\n" in all_row_text:
            contact_name, status_text = all_row_text.splitlines()
        else:
            contact_name, status_text = all_row_text, ""
        row.extend([contact_name, status_text])
        print("FOUND:", "contact name:", contact_name, "status text:", status_text)

        #search photo
        src_pic = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[1]').get_attribute("outerHTML")
        good_url = handle_image_url(src_pic)
        if len(good_url) > 2:
            print("pic")
            with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
                myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + "pic" + "\n")
            sleep(randint(1, 2))
            # open the picture in new tab
            driver.execute_script('''window.open("''' + good_url + '''","_blank");''')
            sleep(randint(1, 2))
            driver.switch_to.window(driver.window_handles[1])
            sleep(randint(1, 2))
            # make screenshot
            driver.save_screenshot("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//" + str(number) + ".jpeg")
            sleep(randint(1, 2))
            # close the new tab
            driver.execute_script('''window.close();''')
            sleep(randint(1, 2))
            driver.switch_to.window(driver.window_handles[0])
            row.append(1)
        else:
            row.append(0)
            print("no pic")
            with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
                myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + "no pic" + "\n")

    row.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open('C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//rowdata.csv', 'a', newline='', encoding="utf-8") as fd:
        writer = csv.writer(fd)
        print(row)
        writer.writerow(row)

    driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input').clear()
    with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//log.txt", "a") as myfile:
        myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + "finish" + " , " + str(number) + "\n")



def main():
    chromedriver = "C:\\Users\\DELL\\Desktop\\chromedriver_new.exe"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://web.whatsapp.com/")
    print("INSERT QR")
    input()
    # move to friends tab
    driver.find_elements_by_class_name("rAUz7")[1].click()
    sleep(randint(5, 10))

    for num_phone in DATA:#range(18569860000, 18569870000):
        try:
            scrape_number(driver, int(num_phone))
        except Exception as e:
            with open("C://Users//DELL//Google Drive//whatsapp_project//whatapp//data//badlog.txt", "a") as myfile:
                myfile.write(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " , " + str(e) + " , " + str(num_phone) + "\n")


if __name__ == '__main__':
    main()