from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc 
from selenium import webdriver

business_name = pd.read_excel('Outlet_Universe_input_file.xlsx', 'Details')
business_name = business_name['Entity_Name'].tolist()

# add user agent 
opts = Options()
opts.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36]")

# # Initializing driver 
driver = uc.Chrome(chrome_options=opts) 
 
# # Try accessing a website with antibot service 
driver.get("https://www.sgpbusiness.com/")
time.sleep(5)
urls,name = [],[]

for i in business_name:
    
    # search business_Name
    search = driver.find_elements(By.ID, "nav_search_val")
    search[0].send_keys(i)

    # click button 
    search_button = driver.find_elements(By.XPATH, "/html/body/nav/div/div/form/div/div[2]/span/button")
    search_button[0].click()

    # # redirect to the next page where we will find the business is live 
    # # scroll down until the element is found

    element = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/a/div/div/h6")
    driver.execute_script("arguments[0].scrollIntoView();", element[0])
    time.sleep(1)
    
    # check condition for single element
    if len(element) <= 1:

        # check if company is alive 
        if 'Live Company' in driver.find_elements(By.CLASS_NAME, "media-body")[0].text.split('\n')[1]:

            # # click on the element
            element[0].click()

            # close the google Vignette
            driver.refresh()

            element = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/a/div/div/h6")
            driver.execute_script("arguments[0].scrollIntoView();", element[0])
            time.sleep(1)
            # # click on the element
            element[0].click()

            # get google map url 
            link = driver.find_elements(By.XPATH, "//div[@class='card-body pb-3']//a[@href]")

            for i in link:
                url = i.get_attribute('href')
                if 'maps' in url:
                    print(url)
                    urls.append(url)
                    name.append(i)
        else:
            urls.append('NA')
            name.append(i)