import time
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()

dump_dict = {'channel': [], 'video_title': [], 'views': [], 'age': []}

f = open('channels.txt', 'r')
for channel in f:
    if channel.split('/')[-1] != 'videos':
        channel = channel + '/videos'
    
    driver.get(channel)

    ht = driver.execute_script("return document.documentElement.scrollHeight;")
    while True:
        prev_ht = driver.execute_script("return document.documentElement.scrollHeight;")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        ht = driver.execute_script("return document.documentElement.scrollHeight;")
        if prev_ht == ht:
            break

    links = driver.find_elements_by_xpath('//*[@id="meta"]')
    print(len(links))
    channel_title = links[0].text.split('\n')[0]
    for link in links[1: -1]:
        if len(link.text.split('\n')) == 3:
            print(f'Канал: {channel_title}')
            video_name = link.text.split('\n')[0]
            print(f'Название видео: {video_name}')
            views = link.text.split('\n')[1]
            print(f'Просмотры: {views}')
            age = link.text.split('\n')[2]
            print(f'Возраст: {age}')
            print('-' * 20)
            
            dump_dict['channel'].append(channel_title)
            dump_dict['video_title'].append(video_name)
            dump_dict['views'].append(views)
            dump_dict['age'].append(age)

pd.DataFrame.from_dict(dump_dict).to_excel('dump.xlsx', index=False)

driver.quit()
