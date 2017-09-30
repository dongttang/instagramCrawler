from bs4 import BeautifulSoup
from selenium import webdriver
import getpass
import time
import wget
import os


def start_crawl():
    user = input("Instagram target user id: ")

    mac_user_id = getpass.getuser()
    default_storage_path = "/Users/{}/Downloads/{}".format(mac_user_id, user)

    default_web_driver_path = "/Users/{}/Downloads/chromedriver" \
        .format(mac_user_id)

    web_driver_path = input("Web driver path(default: {}): ".
                            format(default_web_driver_path))

    if web_driver_path == "":
        web_driver_path = default_web_driver_path

    path = input("Storage path(default: {}/): ".format(default_storage_path))
    local_storage_path = path if path != "" else default_storage_path

    target_url = "http://picbear.com/{}".format(user)

    html_page = load_html_page(target_url, web_driver_path)
    src_url_list = extract_src_url_list(html_page)
    download_pics(src_url_list, local_storage_path)


def load_html_page(target_url, web_driver_path):

    driver = webdriver.Chrome(web_driver_path)

    driver.get(target_url)

    counter = 1

    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[3]/div[2]/div["
                                         "2]/div/p/span")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            print("loading more pages...{}".format(counter))
            counter += 1
            time.sleep(1)
        except:
            break

    return driver.page_source


def extract_src_url_list(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')

    grid_media_list = soup.find_all(class_="grid-media")
    extracted_src_list = list()

    for i in grid_media_list:
        src = str(i).split("src")[1][2:].split("\"")[0]
        if src[0:4] == "http":
            extracted_src_list.append(src)

    return extracted_src_list


def download_pics(target_src_url_list, storage_path):

    path = str(storage_path)

    if not os.path.isdir(path):
        os.mkdir(path)

    for url in target_src_url_list:
        name = wget.download(url, path)

        print(name)


start_crawl()
