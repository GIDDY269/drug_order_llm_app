import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException
import time

def order_automation(items:[]):
    url = 'https://glovoapp.com/ng/en/lagos/medplus-pharmacy-los/'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.chromedriver_executable = "venv/chromedriver-win64/chromedriver.exe"
    try:
        driver = Chrome()
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        time.sleep(10)
        cookie = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']"))
                ).click()
        
        for drugs in items:
            print(f'Ordering {drugs[0]}')
            drug_name = drugs[0]
            number_of_order = drugs[1]

            search_elements = driver.find_elements(By.CLASS_NAME,'search-input__field')

            for search_input in search_elements:
                try:
                    # Wait for the element to be clickable
                  #  search_input = wait.until(EC.element_to_be_clickable((By.ID, search_input.get_attribute("id"))))

                    if wait.until(EC.element_to_be_clickable((By.ID, search_input.get_attribute("id")))):
                        # If the element is interactable, send keys
                        search_input.send_keys(drug_name)
                    


                        # wait for search results
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'list__container')))

                    
                    search_result = driver.find_element(By.CLASS_NAME,'product-row')  # the issues maybe here , foe not clicking on the item


                    if search_result.find_element(By.CLASS_NAME,'product-row__name').text == drug_name: #check if name matches
                            
                        order_count = 1
                        while order_count <= number_of_order:
                            print(f'Number of orders made : {order_count}')
                                
                            search_result.click() 
                                
                            # excutes when there is a add location overlay
                            path_element = wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[data-v-60bfb9dd]'))
                                    )
                    
                            if order_count == 1: 
                                 path_element.click() 
                            else:
                                pass
                            #clicks on add to cart button 
                            add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='helio-button custom-submit primary custom-submit--centered']"))).click()
                            driver.implicitly_wait(20)
                            order_count += 1
                        
                    
                    
                    # restarts the search for another drug
                    driver.find_element(By.XPATH,"//*[@id='default-wrapper']/div/div/div/section[1]/div[2]/div/div[3]/div[1]/div[2]/div/form/img").click()


                    break

                except Exception as e:
                    # Handle the exception if the element is not clickable
                    print(f"Element not clickable: {e}")

            
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException) as e:
        print(f"Exception occurred: {type(e).__name__} - {str(e)}")
    finally:
        driver.quit()





if __name__ == '__main__':
    order_automation([('Postinor *2 Tabs',3),('Ellaone 30Mg *1Tab',4)])

            

            