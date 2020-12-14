from selenium import webdriver
import time
import string
import re
import csv
import pandas as pd
import winsound

# Main menu
mainMenu = {
    1: "Hà Nội",
    2: "TP. Hồ Chí Minh",
    3: "Hội An",
    4: "Đà Lạt",
    5: "Đà Nẵng",
    6: "Nha Trang",
    7: "Vũng Tàu",
    8: "Quảng Ninh"
}

# Finding-location function
def location(selection):
    if selection == 1:
        link = 'a[href="/vi/vietnam/ha-noi"]'
    elif selection == 2:
        link = 'a[href="/vi/vietnam/ho-chi-minh"]'
    elif selection == 3:
        link = 'a[href="/vi/vietnam/quang-nam/hoi-an"]'
    elif selection == 4:
        link = 'a[href="/vi/vietnam/lam-dong/da-lat"]'
    elif selection == 5:
        link = 'a[href="/vi/vietnam/da-nang"]'
    elif selection == 6:
        link = 'a[href="/vi/vietnam/khanh-hoa/nha-trang"]'
    elif selection == 7:
        link = 'a[href="/vi/vietnam/ba-ria-vung-tau/vung-tau"]'
    else:
        link = 'a[href="/vi/vietnam/quang-ninh"]'
    return link

# Print the mainMenu
for x in mainMenu:
    print(x, ":", mainMenu[x])
i = int(input("Chọn địa điểm: "))

# Open webdriver
browser = webdriver.Edge(executable_path="D:/Coding_WorkSpace/NLCS/Luxstay_new/msedgedriver.exe")
browser.get("https://luxstay.com/vi/s")
time.sleep(10)

# Click the next-button if i = 6,7,8
if i in range(6,9):
    next_bt = browser.find_element_by_xpath('//*[@id="mapWrap"]/div[4]/div/div/div[2]/div/button[2]')
    next_bt.click()
    time.sleep(0.5)
    next_bt.click()
    time.sleep(0.5)
    next_bt.click()
    time.sleep(0.5)

# Find the location and click it
link1 = location(i)
location = browser.find_element_by_css_selector(link1)
location.click()
time.sleep(3)

# Declare list
roomName_raw = []
roomName = []
roomPrice_raw = []
roomPrice = []
roomType = []
promotion = []
promotion_raw = []
type_N_rating_raw = []
score = []
review = []
reviews = []
rating = []
bedroom = []

# Get number of loop
browser.switch_to_window(browser.window_handles[1])
time.sleep(7)
page = browser.find_element_by_css_selector('div[class="mt--12 mb--12 text--center text-lowercase"]').text
numofLoop = int(int(page[16:-6])/20)

# GET RAW_DATA:
c = 0
while(True):
        # 1. Room Name
    names = browser.find_elements_by_css_selector('div[class="promo__title"]')
    for element in names:
        roomName_raw.append(element.text)

        # 2. Room Price
    prices = browser.find_elements_by_css_selector('div[class="promo__price mb--6"]')
    for element in prices:
        roomPrice_raw.append(element.text)

        # 3. Room Rating & Type
    type_and_rating = browser.find_elements_by_css_selector('div[class="p--small-2"]')
    for element in type_and_rating:
        type_N_rating_raw.append(element.text)

        # 4. Room promotion
    promo = browser.find_elements_by_css_selector('div[class="is-absolute promo__label-wrap"]')
    for element in promo:
        promotion_raw.append(element.text)
    time.sleep(1)
    c+=1
    if c < numofLoop+1:
        # Click the Next-button:
        next_button = browser.find_element_by_css_selector('li[class="page-item search-next"]').click()
        time.sleep(2)
    else: break

#----------------------------------------------
# HANDLING DATA
    # 1. Prices:
for s in roomPrice_raw:
    s1 = re.sub('"|,|₫/đêm','',s)
    roomPrice.append(s1)

    # 2. Promotion:
for prm in promotion_raw:
    if prm == '':
        promotion.append(0)
    else:
        promotion.append(int(prm[1:-9])/100)

    # 3. RoomType:
roomtype_dict = {
    'Chung cư': 1,
    'Nhà riêng': 2,
    'Homestay': 3,
    'Căn hộ dịch vụ': 4,
    'Studio': 5,
    'Biệt thự':6
}
for e in type_N_rating_raw:
    sub_str = e.split('\n')
    type_sub = sub_str[0].split(" - ")
    if type_sub[0] in roomtype_dict:
        roomType.append(roomtype_dict.get(type_sub[0]))

    # 4. Bedroom:
    bedroom_sub = type_sub[1].split(" ")
    bedroom.append(bedroom_sub[0])

    # 5. Score:
    if len(sub_str) == 1:
        sub_str = sub_str + ['0  (0)']
    rating.append(sub_str[1])
for i1 in rating:
    sub_str1 = i1.split()
    score.append(sub_str1[0])

    # 6. Number of reviews:
    review.append(sub_str1[1])
for rv in review:
    rv1 = re.sub(r'\(|\)', '', rv)
    reviews.append(rv1)

    # 7. Room names
for n in roomName_raw:
    n1 = re.sub('⭐|★|❤|✨|✳️|☂️|❣|❁‿❁|❀|♥️|☃️|❄️|✿|♕|✿|❦|☆|♛|⚡|❃|乂|🌸|✯|🥀|🥳|<|p|>|strong|/|☀', '', n)
    n2 = re.sub('"|,|❣️|✩|☘️|♥|⚜️|⛩️', " ", n1)
    roomName.append(n2)



# Write out csv file
rows = zip(roomName, roomType, bedroom, roomPrice, score, reviews, promotion)
header = ['name', 'type', 'bedroom', 'price', 'score', 'review', 'promo']

# Name the file depend on we input
def csv_name(csv_n):
    if csv_n == 1:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_hanoi.csv'
    elif csv_n == 2:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_tphcm.csv'
    elif csv_n == 3:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_hoian.csv'
    elif csv_n == 4:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_dalat.csv'
    elif csv_n == 5:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_danang.csv'
    elif csv_n == 6:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_nhatrang.csv'
    elif csv_n == 7:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_vungtau.csv'
    else:
        name = 'D:\\Coding_WorkSpace\\NLCS\\csv\\luxstay_quangninh.csv'
    return name

name = csv_name(i)
df = pd.DataFrame(rows)
df.to_csv(name, index=True, header=header)

time.sleep(7)

browser.close()
for sound in range(3):
    winsound.Beep(3000, 600)

