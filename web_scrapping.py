#importing necessary packages
#Selenium - Powerful tool for automation which helps to communicate between the browser and driver
#BeautifulSoup - Is a Python library for pulling data out of HTML and XML files
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


#Remember the code can be further changed and thus can increase its functionality.
#Example using Explicit Wait function of selenium to let the required classes to load before scrapping
#Using the click function of selenium.
#Using try,except block to make the program more readable.


#URL from which data is to be scrapped.
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=Kolkata&BudgetMin=15-Lacs&BudgetMax=90-Lacs"


#Creating a chrome driver
#Pls ensure you have chrome driver installed and you are giving the correct path/
driver = webdriver.Chrome("C:/chrome_driver/chromedriver.exe")



driver.get(url)


#As magic bricks website is  dynamic  we need to scroll down to load the whole page
#Using selenium we scroll down the page to load the whole HTML.
y = 500
for timer in range(0,500):
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 500
    print(timer)
    time.sleep(1)

#Function which helps in scrapping the page.
#Returning the data in the form of a list, later saving it as a CSV file.

def get_data():
    print("Hi! Inside the functioon");

    #Now after loading the whole page.
    #We parse the page HTML using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #List which stores the data scraped.
    all = []

    #d refers to div tag inside the HTML page which acts as container.
    #The container contains a list of all the type of properties with there data. Properties mention Houses
    for d in soup.find_all('div', class_="flex relative clearfix m-srp-card__container"):


        print("I am doing my work pls wait dont close me pls pls pls!!!")
        #Stores the scrapped data of each iteration.
        all_data = []



        #div_of_price contains in it the price and sq_ft details
        div_of_price = d.find('div', class_="m-srp-card__info flex__item")
        #Getting the price insie the div_of_price
        price = div_of_price.find('div', class_="m-srp-card__price").text
        # Getting the sq_ft_area insie the div_of_price
        sq_ft = (div_of_price.find('span', class_="semi-bold"))




        #Getting the no. of rooms information.
        #Using the d variable which iterates each box of a container.
        rooms = d.find('span', class_="m-srp-card__title__bhk").text



        # Getting the total_sq_ft area, floor_no and transaction type
        div_features = d.find('div', class_="m-srp-card__summary js-collapse__content")

        total_sq_ft = (div_features.find_all('div', class_="m-srp-card__summary__info")[0]).text

        floor = (div_features.find_all('div', class_="m-srp-card__summary__info")[2]).text




        #After collecting the necessary data.
        #Grouping the info in a single list:
        all_data.append(price)

        #Storing the sq_ft info in the list
        #If it is None we store it as zero.
        #Later it can be deleted or changed as per need.
        if sq_ft is not None:
            all_data.append(sq_ft.text)
        else:
            all_data.append('0')

        all_data.append(rooms)
        all_data.append(total_sq_ft)
        all_data.append(floor)
        all.append(all_data)
    return all


#Creating a list which stores the data returned from the function.
results = []
results.append(get_data())

#Letting the driver rest.
time.sleep(5)



#Converting the result list into a csv file using pandas.
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Price', 'SuperBuild' , 'BHK' , 'Total_Sq_Ft' , 'Floor'])
df.to_csv('magic_bricks.csv', index=False, encoding='utf-8')



#Thank You.
#Do note Web Scrapping is illegal for some websites
#So pls go through the https://website-name/robots.txt page
#To find out if WebScraping is allowed or not.



