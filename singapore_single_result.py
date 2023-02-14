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

# find out the results 
data= []

for i in new_name:
    
    print("For this url",i)  
    # search business_Name
    search = driver.find_elements(By.ID, "nav_search_val")
    try:
        search[0].send_keys(i)
    except:
        time.sleep(8)
    # click button
    search_button = driver.find_elements(By.XPATH, "/html/body/nav/div/div/form/div/div[2]/span/button")
    try:
        search_button[0].click()
    except:
        time.sleep(8)
        
    try:
        list_ = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[3]/div/div')
        time.sleep(1)
        result = list_[0].text.split('\n')
        print(result)
        print(len(result))
        # for no result 
    except:
        print("except")
        store=["error found on page" for i in range(5)]
        store.append(i)
        data.append(store)
        
    store=[]
    # for no result
    if len(result)==1:
        print("No")
        store=["Not Found" for i in range(4)]
        store.append(" ")
        store.append(i)
        data.append(store)


    # for single result found
    elif len(result)==2: 
        time.sleep(1)
        href = driver.find_elements(By.XPATH, '//div[@class="list-group list-group-flush"]/a')

        c = 0
        l = []
        for d in href:
            dict_details = {}
            dict_details['name'] = result[c]
            dict_details['status'] = result[c + 1].split("U")[0]
            dict_details['registered']='Registered' in result[c + 1].split("U")[0]
            dict_details['url'] = d.get_attribute('href')
            l.append(dict_details)
            c += 2

        for j in l:
            store = []
            if (j['registered'] or j['status'].startswith('Live')):
                driver.get(j['url'])
#                 print(j['url'])
                time.sleep(8)
                try:
                    link = driver.find_element(By.XPATH, "//*[@id='Contact-Information']/div/ul/li/span/small/a")
                    store.append(link.get_attribute('href'))        
                except:
                    try:
                        link=driver.find_element(By.XPATH, "//*[@id='Contact-Information']/div/ul/li[2]/ul/li[1]/span/small/a")
                        store.append(link.get_attribute('href'))        
                    except:
                        store.append('NA')

                try:
                    # Address
                    store.append(driver.find_elements(By.XPATH, "//span[contains(@itemprop, 'address')]")[0].text)
                except:
                    store.append('NA')
                try:
                    # Buiness_name
                    store.append(driver.find_element(By.XPATH,'//*[@id="Overview"]/div[1]/h1').text)
                except:
                    store.append('NA')
                store.append("Found")
                store.append('1')
                store.append(i)
                data.append(store)
            else:
                time.sleep(1)
                store=["Not Found" for i in range(2)]
                store.append(i)
                store.append("Found")
                store.append('0')
                store.append(i)
                data.append(store)
#               

    else:
         
        time.sleep(1)
        # for multiple result found
        href = driver.find_elements(By.XPATH, '//div[@class="list-group list-group-flush"]/a')
        time.sleep(1)
        f=0          
        c = 0
        l = []
        for d in href:
            dict_details = {}
            dict_details['name'] = result[c]
            dict_details['status'] = result[c + 1].split("U")[0]
            dict_details['registered']='Registered' in result[c + 1].split("U")[0]
            dict_details['url'] = d.get_attribute('href')
            l.append(dict_details)
            time.sleep(1)
            c += 2
        for j in l:
            store = []
            if (j['registered'] or j['status'].startswith('Live')) and ('FOOD' in j['name'] or 'BAR' in j['name'] or 'RESTAURANTS' in j['name'] or 'DISCO' in j['name'] or 'LIQUOR' in j['name'] or 'CLUB' in j['name'] or 'WINE' in j['name']):
                driver.get(j['url'])
                time.sleep(8)

                try:
                    link = driver.find_element(By.XPATH, "//*[@id='Contact-Information']/div/ul/li/span/small/a")
                    store.append(link.get_attribute('href'))        
                except:
                    try:
                        link=driver.find_element(By.XPATH, "//*[@id='Contact-Information']/div/ul/li[2]/ul/li[1]/span/small/a")
                        store.append(link.get_attribute('href'))        
                    except:
                        store.append('NA')
                try:
                    store.append(driver.find_elements(By.XPATH, "//span[contains(@itemprop, 'address')]")[0].text)
                except:
                    store.append('NA')
                try:
                    store.append(driver.find_element(By.XPATH,'//*[@id="Overview"]/div[1]/h1').text)
                except:
                    store.append('NA')
                store.append("Found")
                store.append('1')
                store.append(i)
                data.append(store)
                f=1
        if f==0:
            store=["Not Found" for i in range(3)]
            store.append("Found")
            store.append("0")
            store.append(i)
            data.append(store)

# show the data 
print(data)
