"""A base selenium webscraper."""

import logging
from typing import Optional
from parsel import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaseScraper:
    """
    A base class for web scraping using Selenium.

    Attributes:
        name (str): The name of the scraper.
        logger (logging.Logger): Logger for the scraper.
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the BaseScraper with a name.

        Args:
            name (str): The name of the scraper.
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.driver = self.init_driver()

    def init_driver(self) -> webdriver.Chrome:
        """
        Initialize the Selenium WebDriver with Chrome options.

        Returns:
            webdriver.Chrome: A configured Chrome WebDriver instance.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")  # Linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess"
        )
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")

        return webdriver.Chrome(options=chrome_options)

    def get_selector(self) -> Selector:
        """
        Get a Parsel Selector for the current page source.

        Returns:
            Selector: A Parsel Selector object for the current page source.
        """
        return Selector(text=self.driver.page_source)

    def get(self, url: str, title_text: Optional[str] = None) -> None:
        """
        Load a webpage and optionally wait for a specific text in the title.

        Args:
            url (str): The URL of the webpage to load.
            title_text (Optional[str]): Text to wait for in the page title.
        """
        self.driver.get(url)
        if title_text is not None:
            WebDriverWait(self.driver, 100).until(
                EC.title_contains(title_text)
            )

    def click(self, xpath: str) -> bool:
        """
        Click on an element specified by the XPath if not already selected.

        Args:
            xpath (str): The XPath of the element to click.

        Returns:
            bool: True if the element was clicked, False otherwise.
        """
        try:
            el = self.driver.find_element(By.XPATH, xpath)
            if el is not None:
                classes = el.get_attribute("class").split(" ")
                if "selected" not in classes:
                    ActionChains(self.driver).move_to_element(
                        el
                    ).click().perform()
                else:
                    self.logger.info("Element already selected.")
                return True
        except NoSuchElementException:
            self.logger.info("Element not found with the given XPath.")

        return False

    def css_wait(
        self, selector: str, time: int = 30
    ) -> webdriver.remote.webelement.WebElement:
        """
        Wait until a CSS element is located.

        Args:
            selector (str): The CSS selector of the element to locate.
            time (int): Maximum wait time in seconds. Default is 30.

        Returns:
            WebElement: The located WebElement.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def element_exists(self, by: By, tag: str) -> bool:
        """
        Check if an element exists by its tag and locator strategy.

        Args:
            by (By): The locator strategy to use.
            tag (str): The tag or identifier to locate the element.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            self.driver.find_element(by, tag)
            return True
        except NoSuchElementException:
            return False

    def __enter__(self) -> "BaseScraper":
        """
        Enter the runtime context related to this object.

        Returns:
            BaseScraper: The scraper instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The traceback object.
        """
        self.driver.quit()
