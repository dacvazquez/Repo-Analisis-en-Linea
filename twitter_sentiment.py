import streamlit as st
import random
import toml
import streamlit as st
import pandas as pd
from datetime import date 
import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pysentimiento import create_analyzer
#import tweetnlp


# Para análisis de sentimiento
sentiment_analyzer = create_analyzer(task="sentiment", lang="es")

df = pd.DataFrame()

def login_twitter(username_text, password_text, topic_text):
    options = ChromeOptions()
    options.use_chromium = True
    driver = Chrome()
    # options = ChromeOptions()
    # options.use_chromium = True
    # driver = webdriver.Chrome()
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(5)
    username = driver.find_element("xpath",'//input[@name="text"]')
    username.send_keys(username_text)
    driver.find_element("xpath",'(//*[@role="button"])[3]').click() # in prevoius block
    
    try:
        time.sleep(10)
        y = driver.find_element("xpath",'//h1//span')
        if(y.text =='Enter your phone number or username'):
            username2 = driver.find_element("xpath",'//input[@name="text"]')
            username2.send_keys(username_text)
            driver.find_element("xpath",'(//*[@role="button"])[2]').click()
    except:
        st.write(" I am in exception and didnt get 'Enter your phone number or username'")
        x = 10

    password =  driver.find_element("xpath",'//input[@name="password"]')
    password.send_keys(password_text)
    driver.find_element("xpath",'(//*[@role = "button"])[4]').click()


    try:
        driver.maximize_window()
        time.sleep(10)
        driver.maximize_window()
        search = driver.find_element("xpath",'//input[@placeholder="Search"]')
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(topic_text)
        search.send_keys(Keys.RETURN)

        df = pd.DataFrame()
        df['Name']=''
        df['Tweet'] = ''
        df['Sentiment'] = ''
        tweet_count = 6
        i = 1
        element = driver.find_element("xpath","//body")
        time.sleep(20)
        while True and i <= tweet_count:
            
            try:
                tweet_name =  driver.find_element("xpath",f'(//*[@data-testid="User-Name"])[{i}]')
                df.loc[i, 'Name'] = tweet_name.text
                    
                tweet_div = driver.find_element("xpath",f'(//*[@data-testid="tweetText"])[{i}]')
                if(tweet_div):
                    #print(driver.find_element("xpath",'(//*[@data-testid="tweetText"])[1]').getText())
                    df.loc[i, 'Tweet'] = tweet_div.text
                    i += 1
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(10)
            except: 
                time.sleep(10)
                tweet_name =  driver.find_element("xpath",f'(//*[@data-testid="User-Name"])[{i}]')
                df.loc[i, 'Name'] = tweet_name.text
                    
                tweet_div = driver.find_element("xpath",f'(//*[@data-testid="tweetText"])[{i}]')
                if(tweet_div):
                    #print(driver.find_element("xpath",'(//*[@data-testid="tweetText"])[1]').getText())
                    df.loc[i, 'Tweet'] = tweet_div.text
                    i += 1
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(10)


        model = tweetnlp.load_model('sentiment', multilingual=True)  # Or `model = tweetnlp.Sentiment()` 
        
        for i in range(1,len(df)+1):
            print("text is...", df.loc[i,'Tweet'])
            
            
            #y = sentiment_pipeline(df.loc[i, 'Tweet'])
            #print('label is..', y[0]['label'])
            print('model sentiment is..', model.sentiment(df.loc[i, 'Tweet']))
            df.loc[i, 'Sentiment'] = str(model.sentiment(df.loc[i, 'Tweet']))
        st.dataframe(df)

        
    except Exception as e:
        st.write(e)
        # driver.maximize_window()
        # time.sleep(10)
        # driver.maximize_window()
        # search = driver.find_element("xpath",'//input[@placeholder="Search"]')
        # search.send_keys(Keys.CONTROL + "a")
        # search.send_keys(Keys.DELETE)
        # search.send_keys(topic_text)
        

   

with st.sidebar:
    username = st.text_input("Username")
    password_text = st.text_input("Password", type = "password")
    topic = st.text_input("topic")
    connect = st.button("Login Twitter",\
                       on_click = login_twitter,
                       args = [username, password_text, topic]
                       )
    if('is_ready'  not in st.session_state):
        st.session_state['is_ready'] = False

    if(st.session_state['is_ready'] == True):
        st.write('Connected!')
        
