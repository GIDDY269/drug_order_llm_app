import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException
from SQL_Database import *
from schema import CreateScrapeSchema




def fetch(url):
    response = requests.get(url)
    return response.text

def get_desc(section_url,img_link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.chromedriver_executable = "venv/chromedriver-win64/chromedriver.exe"


    max_attempts = 2
    try:
        driver = Chrome(options=chrome_options)
        driver.get('https://glovoapp.com' + section_url)
        page_source = driver.page_source
    
        cookie = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']"))
        ).click()
       
        elements = WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tile']//img[contains(@class, 'tile__image store-product-image')]"))
            )
        
        product_list = [] # Initialize an empty list to store dictionaries for each product
        
        for element in elements:
            
            WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='tile']//img[contains(@class, 'tile__image store-product-image')]"))
            )

            element.click()
        
            path_element = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'path[data-v-00c725c8]'))
             ).click()
            
            driver.implicitly_wait(50)
            name = driver.find_element(By.XPATH,"//h1[@class='product-details__name']").text.strip()
            price = driver.find_element(By.XPATH,"//span[@class='product-price__effective size-large']").text.strip()
            desc = driver.find_element(By.XPATH, "//div[@class='product-details__description product-details__description--centered']").text.strip()


            product_dict = {
                'name' : name,
                'price' : price,
                'description' : desc,
                'image': img_link['src']
            }
            product_list.append(product_dict)

            print('================================================================================')
            print(product_dict)
            print('===============================================================================')
        
            des_element = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'path[data-v-00c725c8]'))
            ).click()
            
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException) as e:
        print(f"Exception occurred: {type(e).__name__} - {str(e)}")
        product_dict = {}
         
    finally:
        driver.quit()

    return product_list

def main():
    url = 'https://glovoapp.com/ng/en/lagos/medplus-pharmacy-los/'
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    for section in soup.find_all('div', class_='store__body__dynamic-content')[1:]:
        header_title_class = ['grid__title', 'carousel__title']
        for title in header_title_class:
            section_name = section.find('h2', class_=title) #gets the section text
            if section_name:
                section_name = section_name.text.strip()
                print(section_name)
                if title == 'grid__title':
                    link = section.find('div', class_='grid__content').find('a').get('href')
                    sub_html = fetch('https://glovoapp.com' + link)
                    sub_soup = BeautifulSoup(sub_html, 'html.parser')
                    for products in sub_soup.find_all('div', class_='tile'):
                        category = sub_soup.find('h2', class_='grid__title').text.strip()
                        img_link = products.find('img')

                    product_list = get_desc(link, img_link) #get product information
                    for product_dict in product_list:
                        product_dict['section'] = section_name
                        product_dict['category'] = category
                        

                        product_data = CreateScrapeSchema(**product_dict).dict()
                        print(f'after pydantic{product_data}')
                        sql_table()
                        insert_data(product_data)
                else:
                    carousel_content = section.find_all('div', class_='carousel__content__element')
                    for content in carousel_content:
                        link = content.find('a').get('href')
                        sub_html = fetch('https://glovoapp.com' + link)
                        sub_soup = BeautifulSoup(sub_html, 'html.parser')
                        category = sub_soup.find('h2',class_='grid__title').text.strip()
                        print(f'Scraping category {category}')
                        grid_content = sub_soup.find('div',class_ = 'grid__content') 
                        for products in grid_content.find_all('div',class_='tile'):
                            img_link = products.find('img')
                        product_list = get_desc(link, img_link) #get product information
                        for product_dict in product_list:
                            product_dict['section'] = section_name
                            product_dict['category'] = category
                            print(f'categorised dict {product_dict}')

                            product_data = CreateScrapeSchema(**product_dict).dict()
                            print(f'after pydantic{product_data}')
                            sql_table()
                            insert_data(product_data)
                print('===============================================')
                continue

if __name__ == "__main__":
    main()







    