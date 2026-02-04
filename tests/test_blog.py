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
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )


def test_blog_homepage_load():
    driver = setup_driver()
    driver.get("https://blog.higo.id")

    # Homepage berhasil load jika heading / konten utama muncul
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

    assert "blog.higo.id" in driver.current_url
    driver.quit()


def test_open_latest_blog_article():
    driver = setup_driver()
    driver.get("https://blog.higo.id")

    wait = WebDriverWait(driver, 15)

    # Tunggu sampai artikel muncul
    articles = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a[href*='/']")
        )
    )

    assert len(articles) > 0, "No blog articles found"

    # Ambil href, JANGAN click element lama
    first_article_url = articles[0].get_attribute("href")

    # Navigate langsung ke URL artikel
    driver.get(first_article_url)

    # Validasi halaman artikel kebuka
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))

    assert driver.current_url != "https://blog.higo.id"

    driver.quit()

def test_blog_has_no_search_feature():
    """
    Negative test:
    Blog HIGO tidak menyediakan search input publik.
    """
    driver = setup_driver()
    driver.get("https://blog.higo.id")

    search_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='search']")
    assert len(search_inputs) == 0

    driver.quit()
