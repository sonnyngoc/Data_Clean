import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import csv
import json, time



def parse(htmlstring, driver, driver1):
    print("-------------------------Start-----------------")
    with open("TIM_DanNormaRentalsQuery.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        line_count = 1
        llc_corp_count = 0

        for row in csv_reader:
            print("Line Count--------------------> : ", line_count)

            if line_count > 1:
                county         = row[0]
                parcel         = row[1]
                buyer_first    = row[2]
                buyer_last     = row[3]
                mail_addr      = row[4]
                mail_city      = row[5]
                mail_state     = row[6]
                mail_zip       = row[7]
                mail_cntry     = row[8]
                sale_date      = row[9]
                sale_price     = row[10]
                legal_class    = row[11]
                legal_subclass = row[12]
                prop_addr      = row[13]      
                prop_city      = row[14]
                prop_state     = row[15]
                prop_zip       = row[16]
                sqr_ft         = row[17]
                con_year       = row[18]
                prop_use       = row[19]    
                
                managerName = ""
                MailingAddress = ""
                option = ""

                data = {
                    "county"         : county,
                    "parcel"         : parcel,
                    "buyer_first"    : buyer_first,
                    "buyer_last"     : buyer_last,
                    "mail_addr"      : mail_addr,
                    "mail_city"      : mail_city,
                    "mail_state"     : mail_state,
                    "mail_zip"       : mail_zip,
                    "mail_cntry"     : mail_cntry,
                    "sale_date"      : sale_date,
                    "sale_price"     : sale_price,
                    "legal_class"    : legal_class,
                    "legal_subclass" : legal_subclass,
                    "prop_addr"      : prop_addr,
                    "prop_city"      : prop_city,
                    "prop_state"     : prop_state,
                    "prop_zip"       : prop_zip,
                    "sqr_ft"         : sqr_ft,
                    "con_year"       : con_year,
                    "prop_use"       : prop_use
                }


                if "llc" in buyer_last.lower() or "corp" in buyer_last.lower():
                    
                    llc_corp_count += 1

                    print("BuyerFirst---------------------> : ", buyer_first)
                    print("BuyerLast----------------------> : ", buyer_last)

                    if buyer_first == "NULL" or buyer_first == "":
                        option = "1st"
                        first_option(driver.page_source, driver, buyer_first, buyer_last)
                    elif buyer_last == "LLC":
                        option = "2nd"
                        second_option(driver.page_source, driver, buyer_first, buyer_last)
                    else:
                        option = "4th"
                        firth_option(driver.page_source, driver, buyer_first, buyer_last)

                    item_counts = len(driver.find_elements_by_class_name("BlueLink"))
                    print("Item Counts-----------------##############--> ", item_counts)
                    # if line_count == 272:
                    #     time.sleep(100)
                    
                    if item_counts == 0 and option != "1st" and option != "2nd":
                        option = "3rd"
                        third_option(driver.page_source, driver, buyer_first, buyer_last)

                    if item_counts > 10 and option != "1st" and option != "2nd":
                        option = "2nd"
                        second_option(driver.page_source, driver, buyer_first, buyer_last)

                    try:
                        pageInfo = driver.find_element_by_class_name("pageinfo").text
                        print("Page Info------------------> : ", pageInfo)    
                        page_array = pageInfo.split(" ")
                        # print(page_array)
                        pageNo = int(page_array[3].replace(",", ""))
                        print("Page Counts----------------> : ", pageNo)
                    except:
                        pageNo = 0

                    # if pageNo == 1:
                    pageNo = pageNo + 1

                    for page in range(1, pageNo):
                        print("Page------------------------> ", page)

                        if page != 1:
                            nextBtn = driver.find_element_by_xpath("//a[contains(text(), 'Next >')]")
                            driver.execute_script("arguments[0].click();", nextBtn)
                            time.sleep(10)

                        item_counts = len(driver.find_elements_by_class_name("BlueLink"))    

                        if item_counts == 0:
                            sr_entity_name = ""
                            sr_name = ""
                            sr_main_address = ""

                            with open("TIM_LLC_CORP.csv", "a", newline="", encoding="utf-8") as f:
                                writer = csv.writer(f)

                                writer.writerow([data["county"], data["parcel"], data["buyer_first"], data["buyer_last"], data["mail_addr"], data["mail_city"], data["mail_state"], data["mail_zip"], data["mail_cntry"], data["sale_date"], data["sale_price"], data["legal_class"], data["legal_subclass"], data["prop_addr"], data["prop_city"], data["prop_state"], data["prop_zip"], data["sqr_ft"], data["con_year"], data["prop_use"], sr_entity_name, sr_name, sr_main_address])

                            with open("TIM_Result.csv", "a", newline="", encoding="utf-8") as f1:
                                writer1 = csv.writer(f1)
                                writer1.writerow([data["county"], data["parcel"], data["buyer_first"], data["buyer_last"], data["mail_addr"], data["mail_city"], data["mail_state"], data["mail_zip"], data["mail_cntry"], data["sale_date"], data["sale_price"], data["legal_class"], data["legal_subclass"], data["prop_addr"], data["prop_city"], data["prop_state"], data["prop_zip"], data["sqr_ft"], data["con_year"], data["prop_use"], sr_entity_name, sr_name, sr_main_address])

                        else:
                            item_urls = driver.find_elements_by_class_name("BlueLink")
                            
                            for item in item_urls:
                                item_url = item.get_attribute('href')
                                print(item_url)

                                driver1.get(item_url)
                                time.sleep(1)
                                parse_info(driver1.page_source, driver1, data)

                    print("llc_corp_count-----------> : ", llc_corp_count)

                    driver.get("https://ecorp.azcc.gov/EntitySearch/Index")

                    entityName = driver.find_element_by_id("quickSearch_BusinessName")
                    entityName.send_keys(Keys.CONTROL, 'a')
                    entityName.send_keys(Keys.DELETE)
                    time.sleep(1)

                else:
                    sr_entity_name = ""
                    sr_name = ""
                    sr_main_address = ""

                    with open("TIM_Result.csv", "a", newline="", encoding="utf-8") as f1:
                        writer1 = csv.writer(f1)
                        writer1.writerow([data["county"], data["parcel"], data["buyer_first"], data["buyer_last"], data["mail_addr"], data["mail_city"], data["mail_state"], data["mail_zip"], data["mail_cntry"], data["sale_date"], data["sale_price"], data["legal_class"], data["legal_subclass"], data["prop_addr"], data["prop_city"], data["prop_state"], data["prop_zip"], data["sqr_ft"], data["con_year"], data["prop_use"], sr_entity_name, sr_name, sr_main_address])
            
            line_count += 1



def parse_info(htmlstring, driver1, data):
    
    all_infos = driver1.find_elements_by_xpath("//div[@class='data_pannel1']//div[contains(@class, 'row')]//div")
    # print(len(all_infos))

    sr_entity_name     = ""
    sr_name            = ""
    sr_address         = ""
    sr_mailing_address = ""
    sr_main_address    = ""

    for i in range(0, len(all_infos)):
        text_info = all_infos[i].text
        if "Name:" == text_info:
            sr_name = all_infos[i+1].text
        elif "Address:" == text_info and sr_address == "":
            sr_address = all_infos[i+1].text
        elif "Mailing Address:" == text_info:
            sr_mailing_address = all_infos[i+1].text
        elif "Entity Name:" == text_info:
            sr_entity_name = all_infos[i+1].text

    if "County" in sr_address:
        sr_address = ""

    if sr_mailing_address == "":
        sr_main_address = sr_address
    else:
        sr_main_address = sr_mailing_address
    
    search_keyword = data["buyer_first"] + data["buyer_last"]
    # flag = destinction(search_keyword.lower(), sr_entity_name.lower())
    
    print("SearchEntityName--------------> : ", sr_entity_name)
    print("SearchName--------------------> : ", sr_name)
    print("SearchAddress-----------------> : ", sr_address)
    print("SearchMailingAddress----------> : ", sr_mailing_address)
    print("SearchMainAddress-------------> : ", sr_main_address)


    # if flag == 2:
    with open("TIM_LLC_CORP.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([data["county"], data["parcel"], data["buyer_first"], data["buyer_last"], data["mail_addr"], data["mail_city"], data["mail_state"], data["mail_zip"], data["mail_cntry"], data["sale_date"], data["sale_price"], data["legal_class"], data["legal_subclass"], data["prop_addr"], data["prop_city"], data["prop_state"], data["prop_zip"], data["sqr_ft"], data["con_year"], data["prop_use"], sr_entity_name, sr_name, sr_main_address])

    with open("TIM_Result.csv", "a", newline="", encoding="utf-8") as f1:
        writer1 = csv.writer(f1)
        writer1.writerow([data["county"], data["parcel"], data["buyer_first"], data["buyer_last"], data["mail_addr"], data["mail_city"], data["mail_state"], data["mail_zip"], data["mail_cntry"], data["sale_date"], data["sale_price"], data["legal_class"], data["legal_subclass"], data["prop_addr"], data["prop_city"], data["prop_state"], data["prop_zip"], data["sqr_ft"], data["con_year"], data["prop_use"], sr_entity_name, sr_name, sr_main_address])


def first_option(htmlstring, driver, buyer_first, buyer_last):
    search_key = buyer_last

    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(search_key)
    time.sleep(2)
    
    searchBtn = driver.find_element_by_id("btn_Search")
    searchBtn.click()
    time.sleep(2)

def second_option(htmlstring, driver, buyer_first, buyer_last):
    driver.get("https://ecorp.azcc.gov/EntitySearch/Index")
    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(Keys.CONTROL, 'a')
    entityName.send_keys(Keys.DELETE)
    time.sleep(1)

    search_key = buyer_first + " " + buyer_last

    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(search_key)
    time.sleep(2)
    
    searchBtn = driver.find_element_by_id("btn_Search")
    searchBtn.click()
    time.sleep(2)

def third_option(htmlstring, driver, buyer_first, buyer_last):
    driver.get("https://ecorp.azcc.gov/EntitySearch/Index")
    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(Keys.CONTROL, 'a')
    entityName.send_keys(Keys.DELETE)
    time.sleep(1)
    
    search_key = buyer_first + " " + buyer_last

    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(search_key)
    time.sleep(2)

    searchBtn = driver.find_element_by_id("btn_Search")
    searchBtn.click()
    time.sleep(2)

def firth_option(htmlstring, driver, buyer_first, buyer_last):
    search_key = buyer_last

    entityName = driver.find_element_by_id("quickSearch_BusinessName")
    entityName.send_keys(search_key)
    time.sleep(2)
    
    searchBtn = driver.find_element_by_id("btn_Search")
    searchBtn.click()
    time.sleep(2)




if __name__ == "__main__":
    
    open("TIM_LLC_CORP.csv", "wb").close()
    header = ["County", "Parcel", "BuyerFirst", "BuyerLast", "MailAddr", "MailCity", "MailState", "MailZip", "MailCntry", "SaleDate", "SalePrice", "LegalClass", "LegalSubClass", "PropAddr", "PropCity", "PropState", "PropZip", "SqrFt", "ConstructionYear", "PropUse", "SrEntityName", "SrName", "SrMAddress"]

    with open("TIM_LLC_CORP.csv", "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames = header, lineterminator='\n')
        csv_writer.writeheader()

    open("TIM_Result.csv", "wb").close()
    header1 = ["County", "Parcel", "BuyerFirst", "BuyerLast", "MailAddr", "MailCity", "MailState", "MailZip", "MailCntry", "SaleDate", "SalePrice", "LegalClass", "LegalSubClass", "PropAddr", "PropCity", "PropState", "PropZip", "SqrFt", "ConstructionYear", "PropUse", "SrEntityName", "SrName", "SrMAddress"]

    with open("TIM_Result.csv", "a", newline="") as f1:
        csv_writer1 = csv.DictWriter(f1, fieldnames = header1, lineterminator='\n')
        csv_writer1.writeheader()

    
    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path, chrome_options = options)
    driver1 = Chrome(executable_path=path, chrome_options = options)

    driver.get("https://ecorp.azcc.gov/EntitySearch/Index")
    driver1.get("https://ecorp.azcc.gov/EntitySearch/Index")
    time.sleep(2)   

    driver.maximize_window()
    driver1.maximize_window()

    parse(driver.page_source, driver, driver1)

