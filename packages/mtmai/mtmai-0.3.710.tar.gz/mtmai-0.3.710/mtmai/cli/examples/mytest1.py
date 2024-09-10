import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_selenium_grid():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.set_capability("browserVersion", "100")
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )
    # driver = webdriver.Chrome()
    # Navigate to a website
    driver.get('https://www.bing.com')

    # Wait for a specific element to be present (e.g., the body tag)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Get the page title
    page_title = driver.title
    print(f"Page title: {page_title}")

    # Find an element and interact with it (e.g., click a button)
    # button = driver.find_element(By.ID, 'some-button-id')
    # button.click()

        # Wait for 2 seconds to see any changes (you can adjust or remove this)
def main():

    test_selenium_grid()
    # Set up Chrome options for connecting to the Selenium Docker container
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')  # Run in headless mode (optional)

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )
    # driver = webdriver.Chrome()
    try:
        # Navigate to a website
        driver.get('https://www.bing.com')

        # Wait for a specific element to be present (e.g., the body tag)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Get the page title
        page_title = driver.title
        print(f"Page title: {page_title}")

        # Find an element and interact with it (e.g., click a button)
        # button = driver.find_element(By.ID, 'some-button-id')
        # button.click()

        # Wait for 2 seconds to see any changes (you can adjust or remove this)
        time.sleep(2)

        # Get the page source
        page_source = driver.page_source
        print(f"Page source length: {len(page_source)}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()