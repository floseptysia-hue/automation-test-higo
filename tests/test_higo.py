from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

def test_homepage_load_successfully():
    driver = setup_driver()
    driver.get("https://higo.id")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "header"))
    )

    assert "higo.id" in driver.current_url
    driver.quit()

def test_navigation_to_blog():
    driver = setup_driver()
    driver.get("https://higo.id")

    original_window = driver.current_window_handle

    blog_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Blog"))
    )
    blog_menu.click()

    # Tunggu tab baru terbuka
    WebDriverWait(driver, 10).until(
        EC.number_of_windows_to_be(2)
    )

    # Switch ke tab baru
    for window in driver.window_handles:
        if window != original_window:
            driver.switch_to.window(window)
            break

    assert "blog.higo.id" in driver.current_url
    driver.quit()

def test_career_menu_redirect_to_linkedin():
    driver = setup_driver()
    driver.get("https://higo.id")

    career_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Karir"))
    )
    career_menu.click()

    WebDriverWait(driver, 15).until(
        lambda d: "linkedin.com" in d.current_url
    )

    assert "linkedin.com" in driver.current_url
    driver.quit()