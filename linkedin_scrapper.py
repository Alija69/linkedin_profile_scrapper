from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

# firstly run "export CHROMEDRIVER=~/chromedriver" in terminal
driver = webdriver.Chrome()
user = "parul@bisresearch.com"
password = "PRL#44559*66"

profile_urls=[]

#read profile urls from excel sheet
df=pd.read_excel(io='/home/alija/Downloads/IM Experts Universal till 11Oct23.xlsx')
for profile_URL in df['linkedin']:
    if isinstance(profile_URL,str):
        profile_urls.append(profile_URL.strip())
profile_urls = profile_urls[:15] 
  
# linkedin login     
def login():
    driver.get("https://linkedin.com/uas/login")
    time.sleep(1)
    username = driver.find_element(By.ID, "username")
    username.send_keys(user) 
    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password)	 
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

# remove \n from text
def clean(str):
    str_list = str.split('\n')
    filtered = [i for i in str_list if i != '' and i!=' '] 
    return " ".join(filtered)

def clean_experience(str):
    str_list = str.split('\n')
    filtered = [i for i in str_list if i != '' and i!=' '] 
    f2 = [i[:len(i)//2] for i in filtered ]
    f2[0] = f'{f2[0]} at'
    return " ".join(f2)

def clean_education(str):
    str_list = str.split('\n')
    filtered = [i for i in str_list if i != '' and i!=' '] 
    f2 = [i[:len(i)//2] for i in filtered ]
    f2[0] = f'{f2[0]},'
    return " ".join(f2)

# returns linkedin profile information
def returnProfileInfo(url):
    try:    
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        main = soup.find('main',class_='scaffold-layout__main')
        sections = main.findAll('section')
        profile = {"name":main.findAll('section')[0].find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() , 
        "location":main.findAll('section')[0].find('span', class_='text-body-small inline t-black--light break-words').get_text().strip(),  
        "headline":main.findAll('section')[0].find('div', class_='text-body-medium break-words').get_text().strip() }
        # import ipdb;ipdb.set_trace()
        for section in sections[1:]:
            try:
                title = section.find('span', class_='visually-hidden').get_text().strip()
                if title=='About':
                    profile["about"]=section.findAll('span', class_='visually-hidden')[1].get_text().strip()
                    profile['about'] = clean(profile['about']) #removing \n
                elif title=='Education':
                    profile['education']=section.find('a', class_='optional-action-target-wrapper display-flex flex-column full-width').get_text().strip()
                    profile['education'] = clean_education(profile['education']) #removing \n
                elif title=='Experience':
                    experiences = section.findAll('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')              
                    profile['experience']=  experiences[0].find('div',class_="display-flex flex-row justify-space-between").get_text().strip()
                    profile['experience'] = clean_experience(profile['experience']) #removing \n
            except Exception as e:
                print(e)
                continue
        return profile
    except Exception as e:
        print(e)

def fetch_experts(URLs):
    try:    
        login()
        time.sleep(18)
        experts_data = []
        error_list=['profile_urls']
        # for profile_url in URLs:
        #     try:
        #         details = returnProfileInfo(profile_url)
        #         details['profile_url'] = profile_url
        #         experts_data.append(details)
        #         time.sleep(2)
        #     except Exception as e:
        #         error_list.append(profile_url)
        #         print(e)
        #         continue
        # df = pd.DataFrame.from_dict(experts_data)
        # df.to_excel('experts.xlsx')
        # with open('error_urls.csv', 'w') as output:
        #     writer = csv.writer(output)
        #     for url in error_list:
        #         writer.writerow([url])
    except Exception as e:
        print(e)
        
fetch_experts(profile_urls)
driver.quit()
