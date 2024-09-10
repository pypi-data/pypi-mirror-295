"""
启动相关后台服务

"""

import logging

from fastapi import APIRouter
from opentelemetry import trace

tracer = trace.get_tracer_provider().get_tracer(__name__)
logger = logging.getLogger()


router = APIRouter()

@router.get("/test")
async def test_selenium():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
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
    return {"title": page_title}
