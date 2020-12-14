from selenium import webdriver
import time
import pandas as pd
import re
import winsound

roomName_raw=[]
roomPrice=[]
type_N_rating=[]
promotion=[]
bedroom=[]
roomType=[]
reviews=[]
score=[]
review=[]
rating=[]
roomName=[]
roomPrices=[]
promotion_percent=[]

# Open webdriver
browser = webdriver.Edge(executable_path="./msedgedriver.exe")
link = 'https://www.luxstay.com/vi/s/?page=1'
browser.get(link)
browser.maximize_window()
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(4)
c = 0
while(True):
        # 1. Room Name
    names = browser.find_elements_by_css_selector('div[class="promo__title"]')
    for element in names:
        roomName_raw.append(element.text)

        # 2. Room Price
    prices = browser.find_elements_by_css_selector('div[class="promo__price mb--6"]')
    for element in prices:
        roomPrice.append(element.text)

        # 3. Room Rating & Type
    type_and_rating = browser.find_elements_by_css_selector('div[class="p--small-2"]')
    for element in type_and_rating:
        type_N_rating.append(element.text)

        # 4. Room promotion
    promo = browser.find_elements_by_css_selector('div[class="is-absolute promo__label-wrap"]')
    for element in promo:
        promotion.append(element.text)
    time.sleep(0.5)
    c+=1
    if c < 50: # Run through  50 pages
        # Click the Next-button:
        next_button = browser.find_element_by_xpath('//*[@id="mapWrap"]/div[5]/div/div/div/div/nav/ul/li[9]/a').click()
        time.sleep(1)    
    else: break

#----------------------------------------------
# HANDLING DATA
    # 1. Prices:
for s in roomPrice:
    s1 = re.sub('"|,|₫/đêm','',s)
    roomPrices.append(s1)

    # 2. Promotion:
for prm in promotion:
    if prm == '':
        promotion_percent.append(0)
    else:
        promotion_percent.append(int(prm[1:-9])/100)

    # 3. RoomType:
roomtype_dict = {
    'Chung cư': 1,
    'Nhà riêng': 2,
    'Homestay': 3,
    'Căn hộ dịch vụ': 4,
    'Studio': 5,
    'Biệt thự':6
}
for e in type_N_rating:
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
    n1 = re.sub('⭐|★|❤|✨|✳️|☂️|❣|❁‿❁|❀|♥️|☃️|❄️|✿|♕|✿|❦|☆|♛|⚡|❃|乂|🌸|✯|🥀|🥳|✦', '', n)
    n2 = re.sub('"|,|❣️|✩|☘️|♥|⚜️|⛩️|❗️', " ", n1)
    roomName.append(n2)


# Write out csv file
rows = zip(roomName, roomType, bedroom, roomPrices, score, reviews, promotion_percent)
header = ['name', 'type', 'bedroom', 'price', 'score', 'review', 'promo']
df = pd.DataFrame(rows)
df.to_csv(r"D:\Coding_WorkSpace\NLCS\csv\10000homestay.csv", sep=",", mode="a",index=True, header=header)
time.sleep(0.25)
    
browser.close()
for sound in range(3):
    winsound.Beep(3000, 600)