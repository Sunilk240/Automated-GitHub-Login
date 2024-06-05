from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv

def login_and_scrape():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open GitHub login page
        driver.get('https://github.com/login')
        print("Opened GitHub login page")

        # Locate the username, password fields, and login button
        username = driver.find_element(By.ID, 'login_field')
        password = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.NAME, 'commit')

        # Enter login credentials
        username.send_keys(os.getenv('GITHUB_USERNAME'))
        password.send_keys(os.getenv('GITHUB_PASSWORD'))

        # Click the login button
        login_button.click()

        # Wait for page to load and check current URL to verify login
        WebDriverWait(driver, 10).until(EC.url_changes('https://github.com/login'))
        current_url = driver.current_url
        if 'login' in current_url:
            print("Login failed: still on login page")
            return
        else:
            print("Login successful")
        
        
        # Navigate to the user's profile page
        driver.get(f'https://github.com/{os.getenv("GITHUB_USERNAME")}')
        print("Navigated to user profile page")

        # Extract profile data
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'p-name'))
        ).text
        bio = driver.find_element(By.CLASS_NAME, 'p-note').text
        followers = driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]/span").text

        # Print extracted data
        print(f"Name: {name}, Bio: {bio}, Followers: {followers}")

        # Save data to a CSV file
        with open('github_profile_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Bio', 'Followers'])
            writer.writerow([name, bio, followers])
        print("Data saved to github_profile_data.csv")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run the scraping function
    login_and_scrape()