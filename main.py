import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_edmc_detailed():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=140)
    
    try:
        driver.get("https://edmc.to/login")
        print("Enter your credentials on the login dialog through the browser...")
        input()
        
        # you should change the base_url for the page you want to scrape from edmc.to
        base_url = "https://edmc.to/genre/riddim-177?page="
        page_number = 1
        
        with open("songs.txt", "a", encoding="utf-8") as f:
            
            while True:
                print(f"Processing page {page_number}...")
                driver.get(f"{base_url}{page_number}")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ipsDataItem"))
                    )
                except:
                    print("End of pages.")
                    break

                rows = driver.find_elements(By.CLASS_NAME, "ipsDataItem")
                
                if not rows:
                    break

                for row in rows:
                    try:
                        link_element = row.find_element(By.CSS_SELECTOR, "span.ipsType_break.ipsContained a")
                        music_url = link_element.get_attribute("href")
                        music_title = link_element.get_attribute("title").strip()

                        time_element = row.find_element(By.TAG_NAME, "time")
                        upload_date = time_element.get_attribute("title")

                        f.write(f"{music_title} ({music_url})\n")
                        f.write(f"{upload_date}\n")
                        f.write("\n")
                        
                    except Exception as e:
                        continue
                
                print(f"Page {page_number} done processing.")
                page_number += 1

    finally:
        driver.quit()
        print("Check file 'songs.txt'.")

if __name__ == "__main__":
    scrape_edmc_detailed()